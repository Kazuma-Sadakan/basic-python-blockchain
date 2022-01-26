import {qs, qsall} from "./utils/dom.utils.js";

const tx_submit = qs("#tx-submit")
const tx_ins = qs("#tx-ins");
const tx_outs = qs("#tx-outs");
const txin_form_create = qs("#txin-form-create").addEventListner
const txout_form_create = qs("#txin-form-create")
let txInFormLength = 1;
let txOutFormLength = 1

txin_form_create.addEventListner("click", createTxInForm)

const createTxInForm = () => {
    const tx_in = document.createElement("div")
    const tx_in_input_hash = document.createElement("input")
    const tx_in_label_hash = document.createElement("label")
    const tx_in_input_index = document.createElement("input")
    const tx_in_label_index = document.createElement("label")
    txInFormLength += 1
    tx_in.classList.classList.add(`tx-in-${txInFormLength}`)

    tx_ins.append(tx_in)
    tx_in.append(tx_in_input_hash)
    tx_in.append(tx_in_label_hash)
    tx_in.append(tx_in_input_index)
    tx_in.append(tx_in_label_index)
}

txout_form_create.addEventListner("click", createTxOutForm)

const createTxOutForm = () => {
    const tx_out = document.createElement("div")
    const tx_out_input_hash = document.createElement("input")
    const tx_out_label_hash = document.createElement("label")
    const tx_out_input_index = document.createElement("input")
    const tx_out_label_index = document.createElement("label")
    txOutFormLength += 1
    tx_out.classList.classList.add(`tx-in-${txOutFormLength}`)

    tx_outs.append(tx_out)
    tx_out.append(tx_out_input_hash)
    tx_out.append(tx_out_label_hash)
    tx_out.append(tx_out_input_index)
    tx_out.append(tx_out_label_index)
}

tx_submit.addEventListner("click", () => {
    
})