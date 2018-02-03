import unittest
from unittest import TestCase

from lib.address import AddressV1
from lib.commons import Network
from lib.keys import PrivateKey


class TestKeys(TestCase):

    def test_to_from_wif(self):
        for n in range(100):
            pk = PrivateKey()
            wif = pk.to_wif(Network.MAIN_NET)
            from_wif = PrivateKey.from_wif(wif)

            self.assertEqual(pk.key, from_wif.key)

    def test_to_from_address(self):
        # Expected address, pub key, private key (WIF)

        vectors = [
            ("1BnxivwaXeg4wfi1Cn8SseJRJ4jJQDQ9rX",
             "0404dfd44f629a806d1c655951f2de58d6fe2180c3b3530e137576c180df74746"
             "b3e62a98051eb8b8aee40bd3f015f10e5f9a9513cbf879e4e357e53736ac4e240",
             "5KjtMvquu4y59HBRN68dsTLrvVWCo4eoW769myKJfFQCtskzrEW"),
            ("16L4aHuU9Krc27qxCEJePAtxomtJPbz21B",
             "042aae9ea9c3aafd929ac41e2ac6a380484347975f6282c5e96c47dfccad609af2"
             "a6d1dee69dc4c4859a1c17fb6e4f22dea3ec65f912efded34192a0b8096ec948",
             "5JDCa6vmWq3TQR9zQtc8P5TsrwAiG3bYe8VpCNQEKVit3QKnXaV"),
            ("1KfvjWLAhJ8PVEysTWUgVaabi6QfB7HSbY",
             "047df6973fb65beb1d3cd6a6bbe0e14c661aa598c61d18d39c152a31cbb84a215"
             "f559653a0e788a62f3a569d5287d8704feb8611869c3f8f65aad521aa0a452a85",
             "5JizFPx2B8L553VmeFf8ujDFw8yA86TVhsHFjfaTk1fAQyGpx34"),
            ("12mM8nzNLEAH6jJSyWwMi7g3sNPXhhB7cR",
             "04f11b5958c4cc1fd483512fe4180c9c97a0fab4c1c43035a0ad21f937f11edf74"
             "918ca64aa952387cff1e7bb045f608e9a57131ecd96e6eb0d18725650a17188d",
             "5Htvi2n8zoJYk7qDeVZg9uotwWEzK27Sck1upESc9xB3Wwnivmk"),
            ("1EyMgCSfVQsMi72d6cYejkZA3AZXMvin1o",
             "04e6396ecf665e9dbc912a133385d7d05795b1ca2b7c1f1dc8b736321a019264fb"
             "3053159b37c180826a490b7cefc0682b924d809d070779a95b16e8de0c745b2c",
             "5JxrhVfBpzLJUkAfnGZhJ4W6zLx1WqniPJ4zN6pGxmjj8McbeKv"),
            ("1358iY8sRB7TzBKtV7Q66KTFJAdfrwCuYx",
             "02ffd9bf5e27f02201c464896a65baea1620ceb9365e7c7291af3ac246044f987a",
             "L2LGS1B2GYeNzFGyrfcKkknNDPd2TQK94JcrM5vEDCBDPgNc7yrJ"),
            ("1JCfRMZ3FKxSQtzVHHhMc5noRGjyzCxq9q",
             "03d747b083ed6124bff391babba647a74451eaafdc4863ca09a9135c7684bc9b42",
             "L5nzmBiuiaS4v1fVT9uxTjhZ9SgQZSqbK4ZbdFGyyiTEHBFqRmiA"),
            ("1MbufYQYxRo7iQTSEdDQSAXG6yHLCgEwr9",
             "03c585e5ad66f92f1028502cc43b987853feb5372ad8fad4c220d977a81ecd2dad",
             "L1i3sweEqFm5wD86tc5w8QS7Fahz8iQTdcaYuf1BUiQowNyb7CvH"),
            ("17A1koGx52oL2c8Dj7DkHeJQ8FfkgczP4R",
             "02a157f7dfeb860be4d4c4a20add1188e537bdb3470fba02ba22e524e7b5e25789",
             "L19vTrnhk1W59u1dk5gry6ixS9G3CgfwPdcgrK4NJbgLnPU31dyr"),
            ("19HJEDUQr4SyBwjqWnYew9wWKKVxZTZZrm",
             "039844cf96d78a177870ddcbc14dfe0b0a63cca1f2a15a6cb9cbee23536721f7b9",
             "KwZhy1ZHYjYri8Tshhwg3XTNjQiSjZbg9tnMPSu8oK6Zhuf3xADj"),
            ("1BCVetosqgdDnR7J5UcFPGDRU1DsYURbGi",
             "0363e91e05cf8cf2000bef64b906eac227fc72746d1d61284310413dd7b3882ec1",
             "L3R7ebrw2EEQcyoiaxuFU53TyZdnrJzzqhkGZUhf9d8zoLPGNxw2"),
            ("1NkHphxqPBMLaUEt9GxFcUYszEgxYPsUpK",
             "03a4a445c703607c987f661e6b93b888b1dbb47286be26391e6684f08f55797304",
             "L1oZuAXaFAi6nD4RkXxFMVGsbHj3fqJekwdUmgGTYCSFzn3939E4"),
            ("1Gr8626DUYfeRrKSzoc1LRYRuexuKzfAT",
             "025ed6ac83aa7b96ed0badcd3b1896c75570fd31fc0b37a564ca5f97771e6f1487",
             "L3NtVYXYEDtBHtaQCLr6Z7uoUq6xb5i5KK5FYmrdMZENd5ZAhu5v"),
            ("13HuVxuwVmqHApzUUr9wU5jBUVuc29y7Kc",
             "03681ca11ab2e3117c2d937eb51e0b8575d44c1d8aaa34b2da4eb518749f3c760d",
             "L19kQsZjzMk2dGUq9Y3HXh4ucDXxeoVecMKEmspS6MqXohHjXfpf")
        ]
        for item in vectors:
            expected_address = item[0]
            public_key_hex = item[1]
            private_key_wif = item[2]

            priv_key = PrivateKey.from_wif(private_key_wif)
            self.assertEqual(private_key_wif, priv_key.to_wif(Network.MAIN_NET))

            pub_key = priv_key.create_pub_key()

            self.assertEqual(pub_key.key.hex(), public_key_hex)

            hash160 = pub_key.hash160()
            address = AddressV1(hash160, Network.MAIN_NET)
            self.assertEqual(address.value, expected_address)


if __name__ == '__main__':
    unittest.main()
