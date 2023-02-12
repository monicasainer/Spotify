# Making My Own Spotify Wrapped!
When the yearly Spotify Wrapped drops you get to see some statistics on music and podcast streaming. We will explore the underlying data for Spotify Wrapped even more by digging into our own streaming history for the past year!

The tool we will be using for visualizing our data is plotly, a Python library which uses a friendly interface to make interactive and pretty graphs. As always when dealing with data we also need to do some data wrangling. For this we will primarily use the library pandas.




# Understand my data
When you use the Download Your Data automated tool, you will receive several files in JSON format. JSON stands for JavaScript Object Notation and is a structured, common format that can be understood by both computers and humans. You can download three different data packages either separately or all at the same time. The packages contain a copy of the following data (if we have this data about you)

## Account data

Data type:

### Playlist

> A summary of the playlists created or saved and songs saved, including:

1. Name of the playlist.
2. The date when the playlist was last changed.
3. Names of songs in the playlist.
4. Names of artists for each song.
5. Name of album or episode (if podcasts).
6. Local names of tracks, if the user has uploaded locally saved audio for playback on the Spotify service.
7. Any description entered by the user for the playlist.
8. Number of followers the playlist has.
9. Streaming history (audio, video and podcasts)

### Streaming history (audio, video and podcasts)

> A list of items (such as songs, videos, and podcasts) that the user has listened to or watched in the past year, including:

1. Date and time when this stream ended in Coordinated Universal Time zone (UTC) format.
2. Name of the "creator" for each stream (eg, the name of the artist if it's a music track).
3. Names of items the user has listened to or watched (eg titles of music tracks or names of videos).
4. "msPlayed" – represents how many milliseconds the track was listened to.

### Your library

> A summary (at the time of request) of the content stored in Your Library (songs, episodes, shows, artists and albums), including:

1. Device name.
2. Name of album and program.
3. Authors.
4. The object's Uniform Resource Identifiers (URIs).
5. Search history

### Search history

> A list of all searches performed, including:

1. Date and time when the search was made.
2. Type of device/platform used (eg iOS, desktop).
3. Search history shows what the user typed in the search field.
4. Search interaction URIs displays the list of Uniform Resource Identifiers (URIs) for the search results that the user has interacted with.
5. See Voice Input below for voice commands.
6. Follow

### Follow

>This includes (if available) at the time of request:

1. The number of followers the account has.
2. The number of other accounts this account follows.
3. The number of other accounts this account has blocked.
4. Payments

### Payments

> This includes payment method information (if available):

1. **Type** – the card type, e.g. MasterCard, Visa, etc. or other type of payment such as gift cards, PayPal.
2. **Card number** - when the payment method is via card, only the last four digits are displayed.
3. **Card expiry date** – when the payment method is via card, the four-digit expiry date is displayed (e.g. 07/18).
4. **Creation date** – the date the payment details were submitted to Spotify.
5. **Payment country** – the country where the card was issued, e.g. Great Britain or Sweden.
6. **Postcode** – the postcode to which the card is registered.

### User data

> This includes (if applicable):

1. Spotify username.
2. Email address.
3. Country.
4. Created from Facebook – this shows if the account was created through Facebook.
5. Facebook User ID – this is included if the user has enabled processing of personal data for Facebook and linked the Spotify account by logging in with Facebook or creating the Spotify account via Facebook.
6. Preferred location.
7. Date of birth.
8. Sex.
9. ZIP code.
10. Postal address.
11. Mobile number.
12. Mobile operator.
13. Mobile brand.
14. When the account was created – this is the date the user signed up.


For more information, click [here]


[here]: https://support.spotify.com/se/article/understanding-my-data/
