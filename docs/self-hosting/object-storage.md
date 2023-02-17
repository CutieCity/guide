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
focused on how to get set up with their service.
![](https://media.cutie.city/custom_emojis/images/000/000/001/original/a74939ddcc369a94.png ":flag_progress:"){.twemoji}

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

Once you've activated your account and successfully signed in, navigate to your
**Buckets** page and create the bucket that will hold all of your instance's
media files. Bucket names have to be unique, so pick something cute and
relevant! (The bucket for [cutie.city] is named `cutiecity`, in case that's a
helpful example.)

Next, navigate to your **Access** page. You should see a menu that looks like
this:

![](/images/storj-access.png "Screenshot of the Access Management page on Storj.
Three sections are displayed: Access Grant, S3 Credentials, and API Key. The
blue action button in the API Key section reads "Create Keys for CLI" and is
circled in pink."){.image-preview data-gallery="storj-access"}

Click the "Create Keys for CLI" button in the **API Key** section (it's circled
in the above screenshot). Put in whatever name you want, check the box to select
<u>all</u> the permissions, and then click the "Create Keys" button. You'll be
shown the resulting **Satellite Address** and **API Key**, but don't worry about
using them right now - just click "Download .txt" and put the file somewhere
safe.

<div class="grid" markdown>
<figure markdown>

![](/images/storj-create-key.png "Screenshot of the "Create Access" modal
dialog. The type is set to "API Access", the name is set to "Kiki" (but this is
unimportant), and the checkbox for "All" permissions is checked and circled in
pink. The remaining options are untouched, and display their default
values."){.image-preview data-gallery="storj-key"}

</figure>
<figure markdown>

![](/images/storj-download-key.png "Screenshot of the success dialog displayed
after clicking the "Create Keys" button in the previous image. The "Satellite
Address" and "API Key" are visible - but don't worry, I've deleted this
particular key! At the bottom, there is a large blue button labeled "Download
.txt". It's circled in pink."){.image-preview data-gallery="storj-key"}

</figure>
</div>

[create a storj account]: https://storj.io/signup
[free plan]:
  https://docs.storj.io/dcs/billing-payment-and-accounts-1/pricing/free-tier
[segments]: https://docs.storj.io/dcs/concepts/definitions
[cutie.city]: https://cutie.city

## Setting up the Uplink CLI

Coming soon!
