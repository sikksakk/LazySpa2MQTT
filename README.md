First version of my LazySpa2MQTT script which I use together with openHAB.

This is just a basic script, feeding values from the API into MQTT subjects.
Plan is to extend it to also be able to turn on/off pump and adjust temp setpoint..
Also my very first python script :-) (so dont kill me..)

Place the script and config in /etc/openhab/scripts (modify the script for config location if different).

Run the script ie. every 30min in a cron.
*/15 * * * * python3 /etc/openhab/scripts/layzspa.py >/dev/null 2>&1

The DID and API_TOKEN is obtained by i.e. using postman (https://www.postman.com/) and using the following settings;
POST https://mobileapi.lay-z-spa.co.uk/v1/auth/login
body; raw with the text: email=asdf%40gmail.com&password=asdf

The API will return a JSON with the following format;
{
    "data": {
        "id": 1111,
        "firstname": "asdf",
        "lastname": "asdf",
        "email": "asdf@gmail.com",
        "address_line1": "null",
        "town": "",
        "county": null,
        "country": "",
        "postcode": "",
        "optin": 1,
        "enabled": true,
        "gizwits_email": null,
        "gizwits_key": null,
        "gizwits_uid": "asdfasdfasdfasdf",
        "gizwits_expires_at": "2020-11-05 06:48:58",
        "gizwits_token": "asdfasdfadsf",
        "created_at": "2020-04-09 23:11:21",
        "updated_at": "2020-05-09 18:22:58",
        "last_login_at": null,
        "api_token-bkp": "",
        "api_token-bkp2": "",
        "api_token": "asdfasdfasdfasdfasdf",
        "full_name": "asdf asdf",
        "anonymous_id": "asdfasdfasdf"
    },
    "devices": [
        {
            "id": 2222,
            "did": "asdfasdfasdfasdf",
            "mac": "D8AAAA261FA",
            "product_key": "asdfasdfasdf",
            "uid": "asdfasdfasdf",
            "user_token": "asdfasdfasdfasdf",
            "app_uid": "2222",
            "created_at": "2020-05-16 22:22:11",
            "updated_at": "2020-05-16 22:22:11",
            "device_name": "My Lay-Z-Spa",
            "pump_type": null
        }
    ],
    "message": "Authorization Successful!"
}

Grab the api_token, and did from devices and use it in the config.

Based on work done by Bruce Hartley;
https://community.home-assistant.io/t/lay-z-spa-hot-tub-wi-fi-pump-automation/229006