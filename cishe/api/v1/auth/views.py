from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView


class HelloView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        content = {"message": "Hello, World!"}
        return Response(content)


class GuestOnlyView(APIView):
    permission_classes = (~IsAuthenticated,)

    def get(self, request):
        # first visit `/`, and then open console in the browser
        # type ```javascript
        # fetch("/api/v1/guest", {
        #     "headers": {
        #         "accept": "application/json,text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        #         "accept-language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7,zh-TW;q=0.6",
        #         "cache-control": "no-cache",
        #         "pragma": "no-cache",
        #         "sec-fetch-dest": "document",
        #         "sec-fetch-mode": "navigate",
        #         "sec-fetch-site": "none",
        #         "sec-fetch-user": "?1",
        #         "upgrade-insecure-requests": "1"
        #     },
        #     "referrerPolicy": "no-referrer-when-downgrade",
        #     "body": null,
        #     "method": "GET",
        #     "mode": "cors",
        #     "credentials": "include"
        # }).then(resp => {console.info(resp, resp.json())});
        # ```
        # and then you will see the cookies in Tab Application of the browser debugger
        # event the devServer(change the `api` to `dev-api`) could proxy the cookie
        content = {"message": "guest only"}
        result = Response(content)
        max_age = 300
        expire_date = datetime.now() + timedelta(seconds=max_age)
        result.set_cookie('test_cookie', 'test_cookie_value',
                          max_age=300, expires=expire_date)
        return result
