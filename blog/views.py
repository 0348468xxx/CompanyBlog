from django.shortcuts import render
from datetime import date

all_posts = [
    {
        'slug': 'first-post',
        'image': '',
        'author': 'Hoa Do',
        'date': date(2020, 1, 1),
        'title': 'First Post',
        'excerpt': 'This is the first post',
        'content': """
                Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                Accusamus, aliquam, atque, autem blanditiis consequuntur cumque
                debitis doloremque dolorum eaque eius enim error esse et eveniet
                explicabo facere fugiat fugit harum hic id illo impedit in
                inventore ipsa ipsum itaque iure laboriosam laborum laudantium
                magnam magni maxime minima minus modi molestias nam natus nemo
                neque nisi nostrum numquam odit officia omnis optio pariatur
                perferendis perspiciatis placeat porro possimus praesentium
                provident quae quam quas quia quibusdam quis quod quos ratione
                recusandae repellendus reprehenderit repudiandae rerum saepe
                sapiente sequi similique sint soluta sunt tempora tenetur
                temporibus, totam ut veritatis voluptas voluptatem voluptatum.
        """
    },

    {
        'slug': 'second-post',
        'image': '',
        'author': 'Hoa Do',
        'date': date(2021, 11, 11),
        'title': 'Second Post',
        'excerpt': 'This is the second post',
        'content': """
                Lorem ipsum dolor sit amet, consectetur adipisicing elit.
                Accusamus, aliquam, atque, autem blanditiis consequuntur cumque
                debitis doloremque dolorum eaque eius enim error esse et eveniet
                explicabo facere fugiat fugit harum hic id illo impedit in
                inventore ipsa ipsum itaque iure laboriosam laborum laudantium
                magnam magni maxime minima minus modi molestias nam natus nemo
                neque nisi nostrum numquam odit officia omnis optio pariatur
                perferendis perspiciatis placeat porro possimus praesentium
                provident quae quam quas quia quibusdam quis quod quos ratione
                recusandae repellendus reprehenderit repudiandae rerum saepe
                sapiente sequi similique sint soluta sunt tempora tenetur
                temporibus, totam ut veritatis voluptas voluptatem voluptatum.
        """
    }
]


def get_date(post):
    return post['date']


def starting_page(request):
    last_posts = sorted(all_posts, key=get_date, reverse=True)
    # last_posts = sorted_posts[-3:]
    return render(request, 'blog/index.html', {
        "posts": last_posts
    })


def posts(request):
    return render(request, 'blog/all-posts.html', {
        "all_posts": all_posts
    })


def post_detail(request, slug):  # Use slug for dynamic URL
    defined_post = next(post for post in all_posts if post['slug'] == slug)
    return render(request, 'blog/post-detail.html', {
        "post": defined_post
    })
