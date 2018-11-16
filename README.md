# Naramispresso

Grouped Nespresso ordering framework based on Typeform.

## Installation

Clone this repository using the following command:

```sh
git clone https://github.com/jguillon/naramispresso.git
```

### Setting up forms

Create a [Typeform](http://typeform.com/) account and [create a personal token](https://admin.typeform.com/account#/section/tokens) for the Typeform API. This token will be used once hereafter.

Automatically generate a Naramispresso form by running the following command:

```sh
curl --request POST \
--header 'Authorization: Bearer <YOUR_PERSONAL_TOKEN>' \
--url https://api.typeform.com/forms \
--data @naramispresso/typeform.json
```

Check your Typeform admin panel to see if the form has been successfully created. Save the form id or URL, as it will be useful for sharing it.

Note that the form may not be up-to-date according to the original Nespresso(R) marcket (especially the limited editions section). Make sure of it before sharing it. Plus, it will be empty of any image, you may want to manually add some by using the ones in the `img/` folder.

### Sending bills

Use the following command to copy `parameters.template.json` in the `parameters.json` file:
```sh
cd naramispresso
cp parameters.template.json parameters.json
```

Then fill in all the field with your personal information.

If you are using your Gmail account to send emails, follow [these instructions](https://stackabuse.com/how-to-send-emails-with-gmail-using-python/) to allow `naramispresso` to use it and optionally get an app-specific password.

## Usage

```sh
./naramispresso.py <CSV_FILE> [--send] [--date <RECEPTION_DATE>]
```
