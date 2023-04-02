$("#cupcake-form").on("submit", async function (event) {
    event.preventDefault();

    const flavor = $("#input-flavor").val();
    const rating = $("#input-rating").val();
    const size = $("#input-size").val();
    const image = $("#input-image").val();

    const createCupcakeResponse = await axios.post('http://127.0.0.1:5000/api/cupcakes', { flavor, rating, size, image });
    $("#cupcake-list").append($(createCupcakeHTML(createCupcakeResponse.data.cupcake)));
    $("#cupcake-form").trigger("reset");
});

function createCupcakeHTML(cupcake) {
    return `
        <div>
        <li>
            Flavor: ${cupcake.flavor} | Size: ${cupcake.size} | Rating: ${cupcake.rating}
        </li>
        <img src="${cupcake.image}" alt="(no image provided)" style="width: 150px; height: 150px;">
        </div>
    `;
}

async function showCupcakes() {
    const response = await axios.get('http://127.0.0.1:5000/api/cupcakes');

    for (let cupcake of response.data.cupcakes) {
        $("#cupcake-list").append($(createCupcakeHTML(cupcake)));
    }
}

showCupcakes()