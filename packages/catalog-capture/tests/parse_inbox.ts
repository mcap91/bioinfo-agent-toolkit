// Tiny cross-check harness: run catalog-mcp's real inbox.ts parser against a file
// path given on argv, so Python tests can assert the TS parser accepts our output
// (not a reimplementation of inbox.ts — the actual parser, per repo convention).
import { readFileSync } from 'node:fs';
import { parseInbox } from '../../catalog-mcp/src/core/inbox.js';

const path = process.argv[2];
const text = readFileSync(path, 'utf-8');
process.stdout.write(JSON.stringify(parseInbox(text)));
