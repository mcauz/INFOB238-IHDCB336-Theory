function delay(time){
    const start = Date.now();
    while (Date.now() - start < time) {}
}

function quick_work(id) {
    delay(5);
    console.log(`quick_work finished: ${id}`);
}

function big_work(callback) {
    setTimeout(() => {
        console.log('big_work finished.');
        callback();
    }, 10000);
}

function do_something_with_big_work_result() {
    delay(5);
    console.log('do_something_with_big_work_result finished.');
}

quick_work("1");
big_work(do_something_with_big_work_result);
quick_work("2");
quick_work("3");
