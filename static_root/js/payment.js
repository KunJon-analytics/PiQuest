console.log('Hello World')

import { Signer } from '@waves/signer';
import { ProviderWeb } from '@waves.exchange/provider-web';

const signer = new Signer({
    // Specify URL of the node on Testnet
    NODE_URL: 'https://nodes-testnet.wavesnodes.com'
});
signer.setProvider(new ProviderWeb('https://testnet.waves.exchange/signer/'))



const wartMaster = 500;
const wartProvider = 1000;


const toggleMasterForm = document.getElementById('toggle-master-form')

toggleMasterForm.addEventListener('submit', e => {
    e.preventDefault()

    $.ajax({
        type: 'POST',
        url: '',
        success: function (response) {
            console.log(response)
        },
        error: function (error) {
            console.log(error)
        }
    })
})