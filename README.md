<h1 align="center">
  <img src="img/naramispresso-logo_200px.png">
  <br>
  Naramispresso
</h1>

<p  align="center">
<em>Grouped Nespresso Purchase Ordering Framework</em>
</p>

## Installation

Clone this repository using the following command:

```sh
git clone https://github.com/jguillon/naramispresso.git
```

### Setting up the form

Create a [Typeform](http://typeform.com/) account and [create a personal token](https://admin.typeform.com/account#/section/tokens) for the Typeform API. This token will be used once hereafter.

Automatically generate a Naramispresso form by running the following command:

```sh
curl --request POST \
     --url https://api.typeform.com/forms \
     --data @naramispresso/typeform.json \
     --header 'Authorization: Bearer <YOUR_PERSONAL_TOKEN>'
```

Check your Typeform admin panel to see if the form has been successfully created. Save the form id or URL, as it will be useful for sharing it.

Note that the form may not be up-to-date according to the original Nespresso(R) marcket (especially the limited editions section). Make sure of it before sharing it. Plus, it will be empty of any image, you may want to manually add some by using the ones in the `img/` folder.

### Setting up the mail service provider

Use the following command to copy `parameters.template.json` in the `parameters.json` file:
```sh
cd naramispresso
cp parameters.template.json parameters.json
```

Then fill in all the field with your personal information.

If you are using your Gmail account to send emails, follow [these instructions](https://stackabuse.com/how-to-send-emails-with-gmail-using-python/) to allow `naramispresso` to use it and optionally get an app-specific password.

## Usage

### Orders summary

Enter the following command to summurize the orders present in the Typeform's `.csv` file. The resulting output will allow you to easilly make your grouped order on [https://www.nespresso.com](http://www.nespresso.com).

```sh
./naramispresso.py <CSV_FILE>
```

### Sending bills

Once you've done the order, you can send the bill to everyone using the following command:

```sh
./naramispresso.py <CSV_FILE> --send --date '<RECEPTION_DATE>'
```

Note that you must specify the reception date using the `--date '<RECEPTION_DATE>'` parameter.

## Custom the form

If you want to add extra coffee brands to the form, you can. The only requirement is to include  its price as a decimal number in the question such as, for example `"AMAZING COFFE (42,00€ / 10 Units)"`. You could have simply put `32987,203838`, it would have worked, but no one will know which coffee brand you were talking about.

## To-do

- [ ] Use Typeform's API to automatically read the latest orders
