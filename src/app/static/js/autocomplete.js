import { Autocomplete, Input, Ripple, initMDB } from "mdb-ui-kit";

initMDB({ Input, Ripple });

const basicAutocomplete = document.querySelector('#search-autocomplete');

var listaDeStrings = results_json.map(function(client) {
    return JSON.stringify({'nome': client.nome, 'cpf': client.cpf});
});

const data = listaDeStrings;
const dataFilter = (value) => {
  return data.filter((item) => {
    return item.toLowerCase().startsWith(value.toLowerCase());
  });
};

new Autocomplete(basicAutocomplete, {
  filter: dataFilter
});