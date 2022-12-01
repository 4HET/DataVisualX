function read_form_session() {
    let fileName = localStorage.getItem('fileName');
    let fileId = localStorage.getItem('fileId');
}
function write_to_session(name) {
    localStorage.clear();
    // return (name);
    localStorage.setItem('name', name);
    console.log(name)
}