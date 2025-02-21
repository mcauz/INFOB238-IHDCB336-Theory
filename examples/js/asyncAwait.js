function myAsynchronousOperation(success, time) {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (success) resolve('It was a great success');
            else reject('It was a great failure');
        }, time);
    });
}

async function myOperation(success) {
    // Do some work
    try {
        const message = await myAsynchronousOperation(success, 3000);
        console.log(message);
    } catch (e) {
        console.error(e);
    }
    // Do some work
}

myOperation(true);
myOperation(false);
