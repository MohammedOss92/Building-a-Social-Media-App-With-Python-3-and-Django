function commentReplyToggle(parent_id) {
    const row = document.getElementById(parent_id);

    if (row.classList.contains('d-none')) {
        row.classList.remove('d-none');
    } else {
        row.classList.add('d-none');
    }
}






function showNotifications() {
    const container = document.getElementById('notification-container');

    if (container.classList.contains('d-none')) {
        container.classList.remove('d-none');
    } else {
        container.classList.add('d-none');
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function removeNotification(removeNotificationURL, redirectURL) {
    const csrftoken = getCookie('csrftoken');
    let xmlhttp = new XMLHttpRequest();

    xmlhttp.onreadystatechange = function () {
        if (xmlhttp.readyState == XMLHttpRequest.DONE) {
            if (xmlhttp.status == 200) {
                window.location.replace(redirectURL);
            } else {
                alert('There was an error');
            }
        }
    };

    xmlhttp.open("DELETE", removeNotificationURL, true);
    xmlhttp.setRequestHeader("X-CSRFToken", csrftoken);
    xmlhttp.send();
}


function formatTags2() {
    const elements = document.getElementsByClassName('body');
    for (let i = 0; i < elements.length; i++) {
        let bodyText = elements[i].children[0].innerHTML;

        let words = bodyText.split(' ');

        for (let j = 0; j < words.length; j++) {
            if (words[j].startsWith('#')) {
                // قم بإنشاء الرابط هنا
                let tag = words[j].substring(1); // إزالة علامة #
                words[j] = `<a href="/tags/${encodeURIComponent(tag)}/">${words[j]}</a>`;
            }
        }

        elements[i].children[0].innerHTML = words.join(' ');
    }
}
function formatTags2222() {
    const elements = document.getElementsByClassName('body');
    for (let i = 0; i < elements.length; i++) {
        let bodyText = elements[i].innerHTML;  // استخدم innerHTML بدلاً من innerText

        // استخدام تعبير منتظم لاستبدال الوسوم
        const replacedText = bodyText.replace(/(#\w+)/g, (match) => {
            const tag = match.substring(1); // إزالة علامة #
            return `<a href="/tags/${encodeURIComponent(tag)}/">${match}</a>`;
        });

        elements[i].innerHTML = replacedText;  // تحديث النص داخل العنصر
    }
}

function formatTags() {
    const elements = document.getElementsByClassName('body');
    for (let i = 0; i < elements.length; i++) {
        let bodyText = elements[i].innerHTML;

        // استخدام تعبير منتظم لاستبدال الوسوم التي تبدأ بـ #
        const replacedText = bodyText.replace(/#(\w+)/g, (match, tag) => {
            return `<a href="/tags/${encodeURIComponent(tag)}/">${match}</a>`;
        });

        elements[i].innerHTML = replacedText;
    }
}

// استدعاء الدالة بعد تحميل الصفحة


// استدعاء الدالة بعد تحميل الصفحة
window.onload = formatTags;

formatTags();