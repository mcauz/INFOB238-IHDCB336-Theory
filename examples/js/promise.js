function myAsynchronousOperation(success, time) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (success) resolve('It was a great success');
        else reject('It was a great failure');
        }, time);
    });
}

myAsynchronousOperation(true, 3000)
    .then((message) => console.log(message), (error) => console.error(error))
    .catch((error) => console.error(error));

myAsynchronousOperation(false, 3000)
    .then((message) => console.log(message), (error) => console.error('1', error))
    .catch((error) => console.error('2', error));

myAsynchronousOperation(false, 3000)
    .then((message) => console.log(message))
    .catch((error) => console.error('2', error));
