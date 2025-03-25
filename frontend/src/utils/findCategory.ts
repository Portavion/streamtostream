import Category from "@/types/category";

export default function (url: string): Category {
  // Example links
  // Track: https://tidal.com/browse/track/126102208?u | https://open.spotify.com/track/3tYxhPqkioZEV5el3DJxLQ?si=56e840f23942422f
  // Album: https://tidal.com/browse/album/126102201?u | https://open.spotify.com/album/6JLO3HVtVEKLHqbgs6ujdw?si=X0bMCFiUQfGEHJilIjCMxA
  // Artist: https://tidal.com/browse/artist/5839856?u | https://open.spotify.com/artist/1IHjrY7ygKbmLVoUV1VcXc?si=Xiouvk-jTHCjmzTfpnxORw
  if (url.includes("track")) {
    return Category.track;
  } else if (url.includes("album")) {
    return Category.album;
    // } else if (url.includes("artist")) {
    // return Category.artist;
  }
  return Category.notFound;
}
