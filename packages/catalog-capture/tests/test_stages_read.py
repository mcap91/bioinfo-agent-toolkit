"""Shared multimodal-read stage (WK-0094 Phase B): `build_stream_message`
must accept an ordered list of images, each with its own media type — the
reel adapter passes one today; the carousel adapter (WK-0087) will pass up
to 20, with no change to this stage. Checked against the real golden-reel
fixtures (the single-image case this package already captured for real),
then generalized to N images to prove the list-of-images contract actually
holds, not just accepts an empty/one-element list by coincidence."""

from __future__ import annotations

import base64
import json
from pathlib import Path

from catalog_capture.stages.read import ReadImage, build_stream_message

FIXTURES_DIR = Path(__file__).parent / "fixtures" / "instagram"
REAL_SHEET = FIXTURES_DIR / "sheet_t0.3.jpg"
REAL_PROMPT = (FIXTURES_DIR / "read_prompt.txt").read_text(encoding="utf-8")


def test_single_real_image_matches_the_existing_real_read_fixture_shape():
    """The reel adapter's exact call shape today: one text block (the real
    captured prompt) followed by one base64 image block for the real
    contact-sheet jpeg — bytes verified against the fixture on disk, not
    re-encoded or assumed."""
    msg = build_stream_message([REAL_PROMPT], [ReadImage(REAL_SHEET)])
    assert msg.endswith("\n")
    obj = json.loads(msg)

    assert obj["type"] == "user"
    assert obj["parent_tool_use_id"] is None
    content = obj["message"]["content"]
    assert len(content) == 2
    assert content[0] == {"type": "text", "text": REAL_PROMPT}
    assert content[1]["type"] == "image"
    assert content[1]["source"]["type"] == "base64"
    assert content[1]["source"]["media_type"] == "image/jpeg"
    assert content[1]["source"]["data"] == base64.b64encode(REAL_SHEET.read_bytes()).decode("ascii")


def test_n_ordered_images_each_keep_their_own_media_type(tmp_path: Path):
    """WK-0087's carousel adapter will pass up to 20 slide images, in order,
    with their own media types (Instagram slides are always JPEG today, but
    the contract itself must not assume that) — this is the forward-looking
    half of the contract, proved here with 3 distinct fake images rather
    than waiting for WK-0087 to exist."""
    images = []
    expected = []
    for i, media_type in enumerate(["image/jpeg", "image/png", "image/jpeg"]):
        ext = "jpg" if media_type == "image/jpeg" else "png"
        path = tmp_path / f"slide_{i}.{ext}"
        data = f"fake-slide-{i}-bytes".encode("ascii")
        path.write_bytes(data)
        images.append(ReadImage(path, media_type=media_type))
        expected.append((media_type, base64.b64encode(data).decode("ascii")))

    msg = build_stream_message(["describe these slides"], images)
    obj = json.loads(msg)
    content = obj["message"]["content"]

    assert len(content) == 1 + len(images)  # one text block, then every image in order
    assert content[0] == {"type": "text", "text": "describe these slides"}
    for i, (media_type, data) in enumerate(expected):
        block = content[1 + i]
        assert block == {"type": "image", "source": {"type": "base64", "media_type": media_type, "data": data}}


def test_no_images_is_a_text_only_message():
    msg = build_stream_message(["just text, no attachments"], [])
    content = json.loads(msg)["message"]["content"]
    assert content == [{"type": "text", "text": "just text, no attachments"}]


def test_images_arg_defaults_to_none_same_as_no_images():
    msg = build_stream_message(["just text"])
    content = json.loads(msg)["message"]["content"]
    assert content == [{"type": "text", "text": "just text"}]
