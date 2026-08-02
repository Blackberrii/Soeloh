"""
Queries the HorizonsRP GMod server via the Source A2S_INFO protocol and
writes the result to status.json at the repo root, so the static site can
fetch it same-origin (no CORS, no API keys). Run on a schedule by
.github/workflows/server-status.yml — stdlib only, no dependencies.
"""
import json
import os
import socket
import sys
from datetime import datetime, timezone

HOST = "193.243.190.4"
PORT = 27087
TIMEOUT = 5
ATTEMPTS = 4  # A2S is UDP — a single reply can arrive truncated/garbled, so retry and validate
OUT_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "status.json")


def read_cstring(data, offset):
    end = data.index(b"\x00", offset)
    return data[offset:end].decode("utf-8", "replace"), end + 1


def query_once():
    payload = b"\xFF\xFF\xFF\xFF\x54Source Engine Query\x00"
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.settimeout(TIMEOUT)
    try:
        sock.sendto(payload, (HOST, PORT))
        data, _ = sock.recvfrom(4096)
        if data[:5] == b"\xFF\xFF\xFF\xFF\x41":
            challenge = data[5:9]
            sock.sendto(payload + challenge, (HOST, PORT))
            data, _ = sock.recvfrom(4096)

        # Reject anything that isn't a well-formed, single-packet A2S_INFO
        # reply — malformed/truncated UDP packets are what produced a
        # bogus player count previously.
        if data[:5] != b"\xFF\xFF\xFF\xFF\x49":
            raise ValueError(f"unexpected response header: {data[:5]!r}")

        off = 6  # header(4) + 'I'(1) + protocol byte(1)
        _name, off = read_cstring(data, off)
        map_, off = read_cstring(data, off)
        _folder, off = read_cstring(data, off)
        _game, off = read_cstring(data, off)
        off += 2  # app id
        players = data[off]; off += 1
        max_players = data[off]; off += 1

        if max_players == 0 or players > max_players:
            raise ValueError(f"implausible player count: {players}/{max_players}")

        return {
            "online": True,
            "players": players,
            "max_players": max_players,
            "map": map_,
        }
    finally:
        sock.close()


def query():
    last_exc = None
    for _ in range(ATTEMPTS):
        try:
            return query_once()
        except Exception as exc:
            last_exc = exc
    raise last_exc


def main():
    checked_at = datetime.now(timezone.utc).isoformat()
    try:
        result = query()
        result["checked_at"] = checked_at
    except Exception as exc:
        result = {"online": False, "checked_at": checked_at, "error": str(exc)}

    with open(OUT_PATH, "w") as f:
        json.dump(result, f, indent=2)
        f.write("\n")

    print(result)


if __name__ == "__main__":
    sys.exit(main())
