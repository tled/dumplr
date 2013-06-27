Dumplr
======

*Dumplr* fetches images from your favorite tumbl blog.

Usage
-----

                    |                /     
                 ___|      _ _  ___ (  ___ 
                |   )|   )| | )|   )| |   )
                |__/ |__/ |  / |__/ | |    
                               |           
              dumps your favorite tumblr blog
    
    usage: dumplr [-h] [-a] [-l BRUTE_FORCE_LIMIT] [--destination PATH]
                  BlogURL [N [N ...]]
    
    Downloads images from a tumblr blog
    
    positional arguments:
      BlogURL               Blog URL, e.g. “foo.tumblr.com”.
      N                     Page(s) to dump. Use “N-M” to specify a range.
    
    optional arguments:
      -h, --help            show this help message and exit
      -a, --all             All blog pages
      -l BRUTE_FORCE_LIMIT, --brute-force-limit BRUTE_FORCE_LIMIT
                            Tries next X pages, if one has no valid images
      --destination PATH, -d PATH
                            Destination directory.

### Examples

Fetching images from blog pages 1, 2, 4, 22, 30, 31, 32, 33, 34, 35:

    dumpl foo.tumblr.com 1-2 4 22 30-35

Fetching images from all pages:

    dumplr -a foo.tumblr.com

Fetching images from all pages and store them in a specific directory:

    dumpl -d my_tumblr_images -a -l 10 http://myblog.tumblr.com

#### What's the ```-l``` option for?

Thus dumplr is not using the tumblr api, it must somehow detect the last page of the blog.
If it requests a blog page, which is out of range, it will get a page without any posts.
So if dumplr gets a page without any valid images, it assumes the ‘end-of-blog‘. But there might be
some blog pages without any image posts, but with a lot of text-only posts. So dumplr will
try the next page until *BRUTE_FORCE_LIMIT* is reached.
