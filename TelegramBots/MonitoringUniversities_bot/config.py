import os


# Bot
API_TOKEN = os.getenv("API_TOKEN", "")

# Monitoring
API_URL = os.getenv('API_URL', "")
HEADERS = {
    'authority': 'vstup.osvita.ua',
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'uk-UA,uk;q=0.9,en-US;q=0.8,en;q=0.7,ru;q=0.6',
    'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'cookie': 'sbr=2; _ga=GA1.2.785814536.1657384432; fnt2=25e032bb1c6b806b6ef9f65248cd99ce; fvbr=Chrome; am-uid=ab904e609aee4abcb09121b73875a101; cto_bundle=09HIIV84QzdUa2VtQ2NYV2RYOGJjeUpJYlhDOVhWVmclMkZBU2FYWTZFbmdwVWx0ZE9ENyUyQjR2anBpSm1RUFBYNHNJWFJiWEJpdyUyQjNhMDFESlNSJTJGNWN3RXJCUHhWcVMwaEdNd3JralA0V3lKSHY2OTRtdlpNU2p6Z1ZrNXVSJTJCSUQzNHJ2S0lNNlQ4NjhUWVJLV2dIeFBCMzhOYnNnJTNEJTNE; _gid=GA1.2.1803689193.1660556259; skdp_986240=f0ec962b5c7f04703b01d88b57e6d508; store.test=; __gpi=UID=00000876e9e028f1:T=1657384433:RT=1660650869:S=ALNI_MbbmJ2V2iK--Z9CcTd4lzPYQR5HOg; b=b; store.test; __gads=ID=fdd4b287896f8bcc:T=1657384433:S=ALNI_MamjU_gWe-vJ3k8HjoVxPL5FuImhw; sdv=1660651553',
    'origin': 'https://vstup.osvita.ua',
    'referer': 'https://vstup.osvita.ua/y2022/r27/174/986240/',
    'sec-ch-ua': '"Chromium";v="104", " Not A;Brand";v="99", "Google Chrome";v="104"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
}
