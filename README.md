# Naramispresso

Grouped Nespresso ordering framework based on Typeform.

## Installation

Clone this repository using the following command:

```shell
git clone https://github.com/jguillon/naramispresso.git
```

### Setting up forms

Create a [Typeform](http://typeform.com/) account and [create a personal token](https://admin.typeform.com/account#/section/tokens) for the Typeform API. This token will be used once hereafter.

Automatically generate a Naramispresso form by running the following command:

```shell
curl --request POST \
--header 'Authorization: Bearer <YOUR_PERSONAL_TOKEN>' \
--url https://api.typeform.com/forms \
--data @naramispresso/typeform.json
```

### Sending bills

If you are using your Gmail account to send emails, follow [these instructions](https://stackabuse.com/how-to-send-emails-with-gmail-using-python/) to allow `naramispresso` to use it and optionally get an app-specific password.


## Usage

```shell
./naramispresso.py <CSV_FILE> [--send] [--date <RECEPTION_DATE>]
```
