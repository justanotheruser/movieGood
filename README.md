# MovieGood

## Utility to dump movie ratings from IMDB and Kinopoisk profile 

# Running

```
    pip install pipenv
    pipenv shell
```

### User mode

```
    python setup.py install
```

### Development mode (with pytest)

```
    python setup.py develop
```

### Usage
```
    py .\movieGood\dump.py --url https://www.imdb.com/user/<your profile here>/ratings 
```

Ratings will be saved into dump folder

