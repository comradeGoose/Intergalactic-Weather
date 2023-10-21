const btn_previous = document.querySelector('#btn-previous');
var btn_index = Number(document.querySelector('#btn-index').textContent);
const btn_next = document.querySelector('#btn-next');

const next = () => {

    if (btn_index === 0) return;
    btn_index -= 1;
    window.location.href = '/page/main?id=' + btn_index;

    fetch('/wallpaper?id=' + btn_index)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            const url = data.url;
            const body = document.body;
            body.classList.add('fade-in');
            setTimeout(() => {
                body.style.backgroundImage = `url('${url}')`;
            }, 500);

            document.querySelector('#btn-index').textContent = btn_index;
            const copyrightLink = document.getElementById('copyright');
            const newHref = data.copyrightlink;
            const newText = data.copyright;
            copyrightLink.href = newHref;
            copyrightLink.textContent = newText;
        })
        .catch(error => {
            console.error('Ошибка при запросе данных:', error);
        });
};

const previous = () => {
    if (btn_index === 6) return
    btn_index += 1
    window.location.href = '/page/main?id=' + btn_index;

    fetch('/wallpaper?id=' + btn_index)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Ошибка HTTP: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log(data);
            const url = data.url;
            const body = document.body;
            body.classList.add('fade-in');
            setTimeout(() => {
                body.style.backgroundImage = `url('${url}')`;
            }, 500);
            document.querySelector('#btn-index').textContent = btn_index;
            const copyrightLink = document.getElementById('copyright');
            const newHref = data.copyrightlink;
            const newText = data.copyright;
            copyrightLink.href = newHref;
            copyrightLink.textContent = newText;
        })
        .catch(error => {
            console.error('Ошибка при запросе данных:', error);
        });
};

btn_previous.addEventListener('click', previous);
btn_next.addEventListener('click', next);