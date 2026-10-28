#!/usr/bin/env python3
"""Validate one saved response and prepare at most one manual format retry."""
import argparse
import hashlib
import json
from pathlib import Path
import sys

EXTENSION = Path(__file__).resolve().parents[1]
ROOT = EXTENSION.parents[3]


def validate(data, schema, path='$'):
    """Cover the constraint vocabulary used by the frozen course schemas."""
    types = {'object': dict, 'array': list, 'string': str}
    kind = schema.get('type')
    if kind in types and not isinstance(data, types[kind]):
        raise ValueError(f'{path}: expected {kind}')
    if kind == 'object':
        for key in schema.get('required', []):
            if key not in data:
                raise ValueError(f'{path}: missing {key}')
        props = schema.get('properties', {})
        if schema.get('additionalProperties') is False and set(data) - set(props):
            raise ValueError(f'{path}: unexpected fields {sorted(set(data) - set(props))}')
        for key, value in data.items():
            if key in props:
                validate(value, props[key], f'{path}.{key}')
    if kind == 'array':
        for index, value in enumerate(data):
            validate(value, schema.get('items', {}), f'{path}[{index}]')


def assess(raw, schema):
    try:
        data = json.loads(raw)
        validate(data, schema)
        return data, None
    except (json.JSONDecodeError, ValueError) as error:
        return None, str(error)


def retry_text(packet, raw, error):
    return (
        'FORMAT REPAIR OF THE SAME RUN; NOT AN INDEPENDENT REPLICATION.\n'
        'Return exactly one JSON object conforming to the original schema. '
        'Correct syntax and field types only. Preserve the substantive claims, '
        'source qualifications and uncertainty. Do not invent missing evidence. '
        'If content is absent, state the limitation in the appropriate field.\n\n'
        f'VALIDATION ERROR\n{error}\n\nORIGINAL PACKET\n{packet}'
        f'\n\nUNEDITED FAILED RESPONSE\n{raw}'
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('response', type=Path)
    parser.add_argument('--attempt', type=int, choices=(0, 1), default=0,
                        help='0 = initial output; 1 = the one allowed format retry')
    parser.add_argument('--packet', type=Path)
    parser.add_argument('--retry-out', type=Path)
    args = parser.parse_args()
    schema = json.loads((ROOT / 'core/output_schema.json').read_text())
    raw = args.response.read_text()
    data, error = assess(raw, schema)
    print('Raw response SHA-256:', hashlib.sha256(args.response.read_bytes()).hexdigest())
    if error is None:
        print('FULL SCHEMA PASSED. Evidence and analytical quality still require review.')
        raise SystemExit(0)
    print('VALIDATION FAILED:', error)
    if args.attempt == 1:
        print('STOP: one format retry exhausted; request human review. No adoption decision.')
        raise SystemExit(2)
    if args.retry_out is not None:
        if args.packet is None:
            parser.error('--packet is required with --retry-out')
        protected = {args.response.resolve(), args.packet.resolve()}
        if args.retry_out.resolve() in protected:
            parser.error('retry output must not overwrite the raw response or original packet')
        args.retry_out.parent.mkdir(parents=True, exist_ok=True)
        with args.retry_out.open('x') as handle:
            handle.write(retry_text(args.packet.read_text(), raw, error))
        print('Prepared one manual retry request; no model was called and raw response is unchanged.')
    else:
        print('Preserve the failed response; use --packet and --retry-out for one manual retry.')
    raise SystemExit(1)
