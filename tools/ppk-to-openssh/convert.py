#!/usr/bin/env python3
"""
Convert an UNENCRYPTED PuTTY private key (.ppk, v2 or v3, RSA) to an OpenSSH key,
without puttygen. Useful when puttygen is not installed on the box.

  python3 ppk-to-openssh.py key.ppk > id_rsa && chmod 600 id_rsa

Parses Public-Lines (ssh-rsa blob: e, n) and Private-Lines (d, p, q), derives the CRT
parameters, and serialises an OpenSSH private key via `cryptography`. Encrypted PPKs
(Encryption != none) are not handled.
"""
import base64, struct, sys
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def parse(path):
    lines = open(path).read().splitlines()
    d, i = {}, 0
    while i < len(lines):
        head = lines[i].split(':', 1)[0]
        if head.endswith('Lines'):
            n = int(lines[i].split(':')[1])
            d[head] = ''.join(lines[i+1:i+1+n]); i += n + 1
        else:
            i += 1
    return d

def rd(b, o):
    ln = struct.unpack('>I', b[o:o+4])[0]; o += 4
    return b[o:o+ln], o + ln

def main(path):
    d = parse(path)
    pub = base64.b64decode(d['Public-Lines'])
    priv = base64.b64decode(d['Private-Lines'])
    _, o = rd(pub, 0); e_b, o = rd(pub, o); n_b, _ = rd(pub, o)
    d_b, o = rd(priv, 0); p_b, o = rd(priv, o); q_b, _ = rd(priv, o)
    to = lambda x: int.from_bytes(x, 'big')
    e, n, dd, p, q = to(e_b), to(n_b), to(d_b), to(p_b), to(q_b)
    key = rsa.RSAPrivateNumbers(p, q, dd, dd % (p-1), dd % (q-1), pow(q, -1, p),
                                rsa.RSAPublicNumbers(e, n)).private_key()
    sys.stdout.buffer.write(key.private_bytes(
        serialization.Encoding.PEM,
        serialization.PrivateFormat.OpenSSH,
        serialization.NoEncryption()))

if __name__ == "__main__":
    main(sys.argv[1])
