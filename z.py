def http_error(status):
    error_string = {
        400: "Bad request",
        404: "Not found",
        418: "I'm a teapot",
    }
    # return error_string.get(status, "Something's wrong with the Internet")
    return error_string.get(status)

print(http_error(400), http_error(418), http_error(444))
k = http_error(444)
print(k)

if not (target := {UC_MAAI: self.maai, UC_DUST: self.dust, UC_AURA: mikoto.aura, UC_FLAIR: mikoto.flair, UC_LIFE: mikoto.life}.get(utuwa_code)):
    raise ValueError(f"Invalid utuwa_code: {utuwa_code}")

target = {UC_MAAI: self.maai, UC_DUST: self.dust, UC_AURA: mikoto.aura, UC_FLAIR: mikoto.flair, UC_LIFE: mikoto.life}.get(utuwa_code, ValueError(f"Invalid utuwa_code: {utuwa_code}"))

