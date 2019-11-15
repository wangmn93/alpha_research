def solve_cf_challenge(resp, **original_kwargs):
    start_time = time.time()

    body = resp.text
    parsed_url = urlparse(resp.url)
    domain = parsed_url.netloc
    submit_url = "%s://%s/cdn-cgi/l/chk_jschl" % (parsed_url.scheme, domain)

    cloudflare_kwargs = copy.deepcopy(original_kwargs)

    headers = cloudflare_kwargs.setdefault("headers", {})
    headers["Referer"] = resp.url

    try:
        params = cloudflare_kwargs["params"] = OrderedDict(
            re.findall(r'name="(s|jschl_vc|pass)"(?: [^<>]*)? value="(.+?)"', body)
        )

        for k in ("jschl_vc", "pass"):
            if k not in params:
                raise ValueError("%s is missing from challenge form" % k)
    except Exception as e:
        # Something is wrong with the page.
        # This may indicate Cloudflare has changed their anti-bot
        # technique. If you see this and are running the latest version,
        # please open a GitHub issue so I can update the code accordingly.
        raise ValueError(
            "Unable to parse Cloudflare anti-bot IUAM page: %s %s"
            % (e.message, BUG_REPORT)
        )

    # Solve the Javascript challenge
    answer, delay = self.solve_challenge(body, domain)
    params["jschl_answer"] = answer

    # Requests transforms any request into a GET after a redirect,
    # so the redirect has to be handled manually here to allow for
    # performing other types of requests even as the first request.
    method = resp.request.method
    cloudflare_kwargs["allow_redirects"] = False

    # Cloudflare requires a delay before solving the challenge
    time.sleep(max(delay - (time.time() - start_time), 0))

    # Send the challenge response and handle the redirect manually
    redirect = self.request(method, submit_url, **cloudflare_kwargs)
    redirect_location = urlparse(redirect.headers["Location"])

    if not redirect_location.netloc:
        redirect_url = urlunparse(
            (
                parsed_url.scheme,
                domain,
                redirect_location.path,
                redirect_location.params,
                redirect_location.query,
                redirect_location.fragment,
            )
        )
        return self.request(method, redirect_url, **original_kwargs)
    return self.request(method, redirect.headers["Location"], **original_kwargs)