var link = "http://127.0.0.1:5000/api/";

// make request type(get, post, etc), data, append to link(id to action(this is how the api works))
function make_request(t, what, d, ap, function_for_data){
	var u = link + what;
	if(ap){
		u += "/" + ap;
	}

	var final_data = 0;
	$.ajax({
		url: u,
		type: t,
		data: d,
		headers: {
			"Content-Type": "application/json" 
		},
		dataType: 'json',
		success: function (data) {
			function_for_data(data);
		}
	});
}

function ver_fechas(nombre, fechas){
	var bts = ""
	fechas.forEach(function(e){
		bts += '<button id="fecha_'+e.id+'">Fecha '+e.numero+'</button>'
		
		
	});

	//document.write(
	//	"<br>" + bts
	//);
	$("body").append("<br>" + bts);
	fechas.forEach(function(e){
	
		$("#fecha_"+e.id).on("click", function(){
			console.log("fecha")
			make_request("get", "fecha", null, e.id, console.log);
		});
	});
	
}

function info_prode(d){
	document.write(
		"<h1>" + d.nombre + "</h1>"
	+	'<button id="boton_participantes">Participantes</button>'
	+	'<button id="boton_fechas">Fechas</button>'
	)

	$("#boton_participantes").on("click", function(){
		console.log("click boton parts");
	});
	$("#boton_fechas").one("click", function(){
		ver_fechas(d.nombre, d.fechas);
	});
}

//get request of all prodes
$(function(){
	$.get(link+"prode", function(data,status){
		data.forEach(function(entry){
			console.log(entry.nombre);
			//var p = $("<p></p>").text(entry.id + "- " + entry.nombre);
			//$("#prodes").append(p);

			$('<button/>', {
				id: entry.id,
				class: "view_prode_"+entry.id,
				html: entry.nombre
			}).appendTo("#prodes");

			$('<button/>', {
				id: entry.id,
				class: "delete"+entry.id,
				html: "x"
			}).appendTo("#prodes");
			$("#prodes").append("<br>");

			$(".delete"+entry.id).on("click", function(){
				make_request("delete", "prode", JSON.stringify({}), entry.id, console.log);
			});

			$(".view_prode_"+entry.id).on("click", function(){
				make_request("get", "prode", null, entry.id, info_prode);
			});
		})
	}, "json")

	// when click nuevo prode, this make a new input box appear
	$("#nuevo_prode").one("click", function(){
		$('<input/>', {
			type: 'text',
			name: 'nuevo_prode_nombre',
			id: "nprode_nombre"
		}).appendTo("#agregar_prode");

		$('<button/>', {
			id: 'boton_nuevo_prode',
			html: "Agregar"
		}).appendTo("#agregar_prode");

		$("#boton_nuevo_prode").one("click", function(){
			var n = $("#nprode_nombre").val();
			make_request('post', "prode", 
				JSON.stringify({
					nombre: n
				}), false, console.log
			);
		});
	});
});