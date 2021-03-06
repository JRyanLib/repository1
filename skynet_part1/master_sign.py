import os
import sys

from Crypto.Signature import PKCS1_v1_5
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA256

# Protect private key with a passphrase
password = "My Secret!"

#Key generation to be run once only
def generate_keys():
    # Generate an 4096 RSA public and private keys.
    generate_key = RSA.generate(bits=4096, e=65537)

    # Get the public key and export it into text file
    public_key = generate_key.publickey().exportKey()
    key_file = open("mypublickey.txt", "wb")
    key_file.write(public_key)
    key_file.close()
    print("Public Key: {}".format(public_key))

    # Get the private key, store with passphrase and export it
    password_private_key = generate_key.exportKey(passphrase=password)

    # Store the export private key into der file type
    key_file = open("myprivatekey.txt", "wb")
    key_file.write(password_private_key)
    key_file.close()
    print("Private Key: {}".format(password_private_key))


def sign_file(f):
    # TODO: For Part 2, you'll use public key crypto here
    # The existing scheme just ensures the updates start with the line 'Caesar'
    # This is naive -- replace it with something better!

    # Retrieve private key from store text file
    read = open("myprivatekey.txt", "r").read()
    private_key = RSA.importKey(read, passphrase=password)

    # Use PKCS#1 as signing scheme with private key for signing
    signer = PKCS1_v1_5.new(private_key)
    digest = SHA256.new(f)  # Hash file with SHA256 algorithm
    sign_file = signer.sign(digest)  # Master bot sign the document with SHA256 hash
    return sign_file


if __name__ == "__main__":
    fn = input("Which file in pastebot.net should be signed? ")
    if not os.path.exists(os.path.join("pastebot.net", fn)):
        print("The given file doesn't exist on pastebot.net")
        sys.exit(1)
    f = open(os.path.join("pastebot.net", fn), "rb").read()
    signed_f = sign_file(f)
    signed_fn = os.path.join("pastebot.net", fn + ".signed")
    out = open(signed_fn, "wb")
    out.write(f + signed_f)
    out.close()
    print("Signed file written to", signed_fn)
