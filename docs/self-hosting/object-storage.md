# Object Storage

This page will walk you through how to get your Mastodon instance set up with an
external **object storage provider** - basically, a media file storage service
in the cloud. This is _technically_ an optional step, but **very highly
recommended**, as it will save you from trouble down the road.

Affordable VPS setups typically aren't very generous with their storage space,
and it isn't efficient to make regular backups of all those media files, so do
your future self a favor and set this up!

In the words of the official [Mastodon documentation]:

> Mastodon can save files that you and your users upload on the hard disk drive
> of the VPS it runs on, however, the hard disk drive is usually not infinite
> and difficult to upgrade later. An object storage provider gives you
> practically infinite metered file storage.

> **How to get:** Amazon S3, Exoscale, Wasabi, Google Cloud, anything that
> exposes either an S3-compatible or OpenStack Swift-compatible API. Comes with
> a monthly cost based on the amount of files stored as well as how often they
> are accessed.

All of those providers are viable choices, as are self-hosted options like
[Garage] and [MinIO]. However, I chose to use [Storj] because I saw a progress
pride rainbow on their website and thought it was cute, so this page will be
focused on how to get set up with their service. :flag_progress:

[mastodon documentation]: https://docs.joinmastodon.org/user/run-your-own/
[garage]: https://garagehq.deuxfleurs.fr/
[minio]: https://min.io/
[storj]: https://www.storj.io/

## Getting started with Storj

The first thing you'll need to do is [create a Storj account]. Make sure the
correct **satellite** (i.e. your geographic region) is selected - currently, the
available options are **US1**, **EU1**, and **AP1**. You don't need to provide
your payment information until you hit the limits of their [free plan]:

- 150GB of static object storage
- 150GB of download bandwidth per month
- 10,000 [segments] in total

### Creating a bucket

Once you've activated your account and successfully signed in, navigate to your
**Buckets** page and create the bucket that will hold all of your instance's
media files. Bucket names have to be unique, so pick something cute and
relevant! (The bucket for [cutie.city] is named `cutiecity`, in case that's a
helpful example. :blobfox_derp_mlem:)

### Obtaining an API key

Next, navigate to your **Access** page. You should see a menu that looks like
this:

![](/images/storj-access.png "Screenshot of the Access Management page on Storj.
Three sections are displayed: Access Grant, S3 Credentials, and API Key. The
blue action button in the API Key section reads "Create Keys for CLI" and is
circled in pink."){.preview data-gallery="storj-access"}

Click the "Create Keys for CLI" button in the **API Key** section (it's circled
in the above screenshot). Put in whatever name you want, check the box to select
^^all^^ the permissions, and then click the "Create Keys" button. You'll be
shown the resulting **Satellite Address** and **API Key**, but don't worry about
using them right now - just click "Download .txt" and put the file somewhere
safe.

<div class="grid two-columns" style="margin-bottom: 0;" markdown>
<figure style="width: 100%;" markdown>

![](/images/storj-create-key.png "Screenshot of the "Create Access" modal
dialog. The type is set to "API Access", the name is set to "Kiki" (but this is
unimportant), and the checkbox for "All" permissions is checked and circled in
pink. The remaining options are untouched, and display their default
values."){.preview data-gallery="storj-key" style="object-position: 0 42%;"}

</figure>
<figure style="width: 100%;" markdown>

![](/images/storj-download-key.png "Screenshot of the success dialog displayed
after clicking the "Create Keys" button in the previous image. At the bottom,
there is a large blue button labeled "Download .txt". It's circled in pink. The
"Satellite Address" and "API Key" are visible. (Don't worry, I've revoked this
particular key!)"){.preview data-gallery="storj-key"}

</figure>
</div>

<p style="margin-top: 0; text-align: center;" markdown>
<small style="font-style: italic;">

**Tip:** Click on any of these images to expand them, or hover over them to view
an image description.

</small>
</p>

[create a storj account]: https://storj.io/signup
[free plan]:
  https://docs.storj.io/dcs/billing-payment-and-accounts-1/pricing/free-tier
[segments]: https://docs.storj.io/dcs/concepts/definitions
[cutie.city]: https://cutie.city

## Navigating the Storj CLI

We're done with the Storj web interface for now! The next steps will make use of
their [Uplink] CLI tool, which provides the easiest way to generate all of the
configuration variables that you need to connect your Mastodon instance to your
Storj bucket.

[uplink]: https://docs.storj.io/dcs/downloads/download-uplink-cli

### Installing Uplink

=== "Linux"

    Execute the following commands in your terminal. (Depending on your
    machine's architecture, you may need to replace `amd64` with `arm` or
    `arm64` in the first two commands.)

    ```console
    curl -L https://github.com/storj/storj/releases/latest/download/uplink_linux_amd64.zip -o uplink_linux_amd64.zip
    ```
    ```console
    unzip -o uplink_linux_amd64.zip
    ```
    ```console
    sudo install uplink /usr/local/bin/uplink
    ```

=== "macOS"

    Execute the following commands in your terminal.

    ```console
    curl -L https://github.com/storj/storj/releases/latest/download/uplink_darwin_amd64.zip -o uplink_darwin_amd64.zip
    ```
    ```console
    unzip -o uplink_darwin_amd64.zip
    ```
    ```console
    sudo install uplink /usr/local/bin/uplink
    ```

=== "Windows"

    1. Download the [Windows binary zip file] for Uplink.

    2. Right-click the downloaded file and select "Extract All". You can put the
       contents in whatever folder you want, but your home folder (i.e.
       `C:\Users\YOUR_NAME`) is recommended.

    3. Don't bother trying to open the `uplink.exe` file - it's only usable via
       the command line.

    4. Open your terminal of choice (e.g. PowerShell) and `cd` into the folder
       where you put the `uplink.exe` file. (If you put it in your home folder,
       you don't need to `cd`.)

[windows binary zip file]:
  https://github.com/storj/storj/releases/latest/download/uplink_windows_amd64.zip

### Running the setup wizard

=== "Linux"

    ```console
    uplink setup
    ```

=== "macOS"

    ```console
    uplink setup
    ```

=== "Windows"

    ```console
    .\uplink.exe setup
    ```

When asked to enter a name, you can leave it blank (i.e. just hit ++enter++).
You'll then be asked for information from the `.txt` file you downloaded
earlier, so open up that file (it should only contain two lines) and use it to
proceed through the following steps.

1. First, you'll need the "API key or Access grant" - this is on the line
   labeled `restricted key` in the text file. Copy and paste its alphanumeric
   value into the setup wizard.

2. Next, you'll need the information on the line labeled `satellite address`.
   Copy and paste this ^^entire^^ value, **including the port number** at the
   end (i.e. `7777`).

3. You'll then be asked to enter and confirm a passphrase. (As far as I can
   tell, this passphrase is only required when you open your project in the
   Storj web interface... but don't forget it!)

4. Finally, you'll be asked whether you'd like S3 backwards-compatible Gateway
   credentials. This is what we're here for, so respond with `y` and you should
   see something like this:

   ```{.console .no-copy}
   ============== GATEWAY CREDENTIALS ==============
   Access Key ID: jklasdfgh12zxcvbnm34ytrewqpo
   Secret Key   : jyuiopqwert123asdfghjkl456zxcvbnm789qwertyuiop0asdfgh
   Endpoint     : https://gateway.storjshare.io
   ```

Make sure to keep these credentials safe! They're what'll give your Mastodon
instance the ability to create and destroy objects in your Storj project, and
you definitely don't want that power to fall into the wrong hands. :kitty_eyes:

### Getting a link-sharing key

Storj's concept of "public buckets" differs slightly from other services. A
unique **link-sharing key** is required in order to view your files from outside
their web interface.

To generate a link-sharing key for your instance's Storj bucket, run the
following command (and **don't forget** to replace `BUCKET` with the name of
[your own bucket](#creating-a-bucket), e.g. `cutiecity`):

=== "Linux"

    ```console
    uplink share --url --readonly --disallow-lists --not-after=none sj://BUCKET
    ```

=== "macOS"

    ```console
    uplink share --url --readonly --disallow-lists --not-after=none sj://BUCKET
    ```

=== "Windows"

    ```{.console .no-copy}
    .\uplink.exe share --url --readonly --disallow-lists --not-after=none sj://BUCKET
    ```

At the end of the resulting CLI output, you should see a section that looks
similar to this:

```{.console .no-copy #linkshare-output}
================== BROWSER URL ==================
URL       : https://link.storjshare.io/s/jwcl3biyuellbunqouyj7g4htdna/cutiecity
```

<script>
  // Surround the link-sharing key with tags to make it appear as bold text.
  const span = document.querySelector("#linkshare-output span:last-child");
  const strong = document.createElement("strong");
  const keyString = span.innerHTML.match(/[a-z0-9]{28}/)[0];
  strong.appendChild(document.createTextNode(keyString));
  span.innerHTML = span.innerHTML.replace(keyString, strong.outerHTML);
</script>

Your link-sharing key is the gibberish-looking part of the URL it spits out -
mine is bolded above, as an example. This is the only piece of information you
need from the command you just ran, so feel free to ignore/discard the rest of
the output.

??? tip "Tip - Don't mix up your keys!"

    Just like the S3 access key you generated in the previous step, your
    link-sharing key should be **28 characters** long. Take care not to confuse
    the two! They serve different purposes and are used throughout the rest of
    this guide.

    As mentioned earlier, your **S3 access key** (when used alongside your **S3
    secret key**) effectively grants complete access to your Storj project. It's
    extremely important to keep these two keys ^^private^^.

    On the other hand, your **link-sharing key** isn't sensitive information, as
    it only allows other people to read (not write) your files in the Storj
    bucket for your Mastodon instance. In fact, if you decide to forgo the
    [last section](#linking-your-domain) of this guide, your link-sharing key
    will be visible in all image/video links from your instance. This is
    perfectly fine and safe! :cozy:

## Configuring Mastodon

Now that you have your link-sharing key and S3 credentials, it's time to plug
them all into your Mastodon environment! Open up your `.env.production` file and
configure your `S3` and `AWS` variables as follows:

```ini title="/home/mastodon/live/.env.production"
S3_ENABLED=true
S3_PROTOCOL=https
S3_REGION=global
S3_ENDPOINT=https://gateway.storjshare.io
S3_HOSTNAME=gateway.storjshare.io
S3_BUCKET=BUCKET
S3_ALIAS_HOST=link.storjshare.io/raw/LINK_SHARING_KEY/BUCKET
AWS_ACCESS_KEY_ID=S3_ACCESS_KEY
AWS_SECRET_ACCESS_KEY=S3_SECRET_KEY
```

Make sure to replace all of the placeholders with the actual values you've
generated for them.

| Placeholder ID     | Explanation                                                                  | Example                                                              |
| ------------------ | ---------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| `BUCKET`           | The name of your bucket. _(Appears twice!)_                                  | `cutiecity`                                                          |
| `LINK_SHARING_KEY` | Your link-sharing key from the [previous step](#getting-a-link-sharing-key). | `jwcl3biyuellbunqouyj7g4htdna`                                       |
| `S3_ACCESS_KEY`    | Your `Access Key ID` from the [setup wizard](#running-the-setup-wizard).     | `jklasdfgh12zxcvbnm34ytrewqpo`{#access-key}                          |
| `S3_SECRET_KEY`    | Your `Secret Key` from the [setup wizard](#running-the-setup-wizard).        | `jyuiopqwert123asdfghjkl456zxcvbnm789qwertyuiop0asdfgh`{#secret-key} |

<script>
  // Limit the width of the secret key example to maintain column proportions.
  const maxWidth = document.querySelector("#access-key").offsetWidth;
  document.querySelector("#secret-key")
    .setAttribute("style", `display: block; max-width: ${maxWidth}px`);
</script>

Once you've finished, **save the file** and then restart the relevant Mastodon
processes:

```console
systemctl restart mastodon-sidekiq && systemctl reload mastodon-web
```

You should now be able to open up your Mastodon instance in your browser and
upload images. They'll go straight to your Storj bucket and be accessible to the
public via link-sharing! :celebrate:

## Linking your domain

Coming soon!
