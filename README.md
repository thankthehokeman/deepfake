# Deepfake 

This project is a working deepfake detector website prototype complete with 3 front pages with differing visual aesthetics, a loading page, and a results page. 

It is created using the flask package and python3

It is meant to emulate a deepfake detector. Thus what the viewer will see is a working detector. However, the "AI" is simply a list 
which checks for flagged file names. 

The viewer can upload a image of their choosing or 20 images from the gallery. This can be done in the front page itself.

The viewer will then be subjected to a loading page which will redirect to the results page after a randomized time of between 1 and 3 seconds.

The results page then will have a box showing the verdict being deepfake or not and the percentage of confidence. 
Below the box are 3 smaller boxes. The left most box has a preview of the uploaded image, the middle box has 4 models with their own confidence levels which are randomized to be slightly off of the percentage of confidence and the right box which contains data about the image.

Using cookies, when the user accesses a front page, they will be locked onto that front page until they clear their cookies.
This manifests when trying to access loading or results when not permitted to and redirects them to the front page link. If they type in the base website link with no sub link, they are redirected.

## Website

We have a link now!

Use this link to access https://monolith-5e1d6ff7b5b6.herokuapp.com/

There are 3 front pages to access:

Neutral: https://monolith-5e1d6ff7b5b6.herokuapp.com/greetings

Good: https://monolith-5e1d6ff7b5b6.herokuapp.com/hello

Bad: https://monolith-5e1d6ff7b5b6.herokuapp.com/hi

WARNING: You must access one of the front pages on first visit to set a front page for the rest of your visit!

## Installation

Create a virtual environment: [venv documentation](https://docs.python.org/3/library/venv.html)

Use the package manager [pip](https://pip.pypa.io/en/stable/) and the requirements.txt to install the required dependencies.

```bash
pip install -r /path/to/requirements.txt
```

## Usage

```python
# returns 'must customize app.run()'
python3 app.py

# easier way of running it
flask run
```
Then check https://127.0.01:5000 or your own custom port which you can customize with

```python
# returns 'must customize app.run()'
if __name__ == "__main__":
    app.run(port="your port here")
```
## Credits

Favicon (Freepik): [Freepik](https://www.freepik.com/free-vector/atlantis-ruins-isolated-compositions-set-ancient-pavilion-rotunda-columns-arch-cartoon-illustration_16396038.htm)

Image of hero background: [Unsplash](https://unsplash.com/photos/gray-concrete-building-illustration-71mBbj1l8ow)

Image of man: [Unsplash](https://unsplash.com/photos/person-in-black-knit-cap-and-gray-sweater-q7ZlbWbDnYo)

Image of woman: [Unsplash](https://unsplash.com/photos/shallow-focus-photography-of-woman-outdoor-during-day-rDEOVtE7vOs)

## License

[MIT](https://choosealicense.com/licenses/mit/)
