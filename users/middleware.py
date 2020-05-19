class Protect:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, *view_args, **view_kwargs):

        if request.path.startswith('/api/user/'):
            print("📌📌📌 middleware")
            print(request.path)
            # protect route logic
