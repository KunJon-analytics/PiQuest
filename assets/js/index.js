import { Signer } from '@waves/signer';
import { ProviderWeb } from '@waves.exchange/provider-web';
const crypto = require('@waves/ts-lib-crypto');

const masterForm = document.getElementById("toggle-master-form");
const updateUrl = window.location.href;

const signer = new Signer();

const getCookie = (name) => {
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
};
const csrftoken = getCookie('csrftoken');

signer.setProvider(new ProviderWeb());

masterForm.addEventListener('submit', e => {
    e.preventDefault()

    const label = document.querySelector(".success-area");
    const masterData = {
        recipient: '3PQc55HLEe2s8eFxz2qy5TjQk6YwGVDLD1T',
        amount: payment * Math.pow(10, 8),
        assetId: '4kXACcTnNJa14Zbs19irgg48G6jR5nWp8SgPndFWY5av',
        attachment: crypto.base58Encode(crypto.stringToBytes(paymentAttachment))
    };

    signer.transfer(masterData).broadcast().then(
        () => {
            $.ajax({
                type: 'POST',
                url: updateUrl,
                data: {
                    'csrfmiddlewaretoken': csrftoken,
                },
                success: function (response) {
                    var sucessUrl = window.location.origin + response.data.url;
                    label.innerHTML = `
                <div class="alert alert-success shadow" role="alert" style="border-left:#155724 5px solid; border-radius: 0px">
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true" style="color:#155724">&times;</span>
                    </button>
                    <div class="row">
                        <svg width="1.25em" height="1.25em" viewBox="0 0 16 16" class="m-1 bi bi-shield-fill-check" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M8 .5c-.662 0-1.77.249-2.813.525a61.11 61.11 0 0 0-2.772.815 1.454 1.454 0 0 0-1.003 1.184c-.573 4.197.756 7.307 2.368 9.365a11.192 11.192 0 0 0 2.417 2.3c.371.256.715.451 1.007.586.27.124.558.225.796.225s.527-.101.796-.225c.292-.135.636-.33 1.007-.586a11.191 11.191 0 0 0 2.418-2.3c1.611-2.058 2.94-5.168 2.367-9.365a1.454 1.454 0 0 0-1.003-1.184 61.09 61.09 0 0 0-2.772-.815C9.77.749 8.663.5 8 .5zm2.854 6.354a.5.5 0 0 0-.708-.708L7.5 8.793 6.354 7.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/>
                        </svg>
                        <p style="font-size:18px" class="mb-0 font-weight-light"><b class="mr-1"> Yipee! Your payment was a success. You can test your powers <a href="${sucessUrl}" class="alert-link"> by following this link.</a></p>
                    </div>
                </div>
            `;
                    console.log(sucessUrl);
                    $("#login-form-area").hide(1000);
                },
                error: function (error) {
                    label.innerHTML = `
                <div class="alert alert-danger shadow" role="alert" style="border-left:#721C24 5px solid; border-radius: 0px">
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true" style="color:#721C24">&times;</span>
                    </button>
                    <div class="row">
                        <svg width="1.25em" height="1.25em" viewBox="0 0 16 16" class="m-1 bi bi-exclamation-circle-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
                        </svg>
                        <p style="font-size:18px" class="mb-0 font-weight-light"><b class="mr-1">Danger!</b>${error}</p>
                    </div>
                </div>
            `;
                    console.log(error);
                }
            });
        },
        (e) => {
            label.innerHTML = `
                <div class="alert alert-danger shadow" role="alert" style="border-left:#721C24 5px solid; border-radius: 0px">
                    <button type="button" class="close" data-dismiss="alert" aria-label="Close">
                        <span aria-hidden="true" style="color:#721C24">&times;</span>
                    </button>
                    <div class="row">
                        <svg width="1.25em" height="1.25em" viewBox="0 0 16 16" class="m-1 bi bi-exclamation-circle-fill" fill="currentColor" xmlns="http://www.w3.org/2000/svg">
                        <path fill-rule="evenodd" d="M16 8A8 8 0 1 1 0 8a8 8 0 0 1 16 0zM8 4a.905.905 0 0 0-.9.995l.35 3.507a.552.552 0 0 0 1.1 0l.35-3.507A.905.905 0 0 0 8 4zm.002 6a1 1 0 1 0 0 2 1 1 0 0 0 0-2z"/>
                        </svg>
                        <p style="font-size:18px" class="mb-0 font-weight-light"><b class="mr-1">Danger!</b>${e}</p>
                    </div>
                </div>
            `;
            console.log(e);
        }
    );
});