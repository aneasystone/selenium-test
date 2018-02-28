
    chrome.proxy.settings.set({
        value: {
            mode: "fixed_servers",
            rules: {
                singleProxy: {
                    scheme: "http",
                    host: "127.0.0.1",
                    port: 8118
                },
                bypassList: ["foobar.com"]
            }
        },
        scope: "regular"
    }, function() {});

    chrome.webRequest.onAuthRequired.addListener(
        function (details) {
            return {
                authCredentials: {
                    username: "",
                    password: ""
                }
            };
        },
        { urls: ["<all_urls>"] },
        [ 'blocking' ]
    );
    