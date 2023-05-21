function getmycontents(){
	$.get("/mycontents2",function(res){
		rs=JSON.parse(res);
		$("#listfiles").html("");
		rs.forEach((e)=>{
			$("#listfiles").append(`<tr><td><img src="/uploads/${e.filename}" width="200px"></td><td>${e.title}</td></tr>`);
			
		});
		
	});
}





$(document).ready(function(){
   


	// afora tin eggrafi tou xristi

	$("#frmegrafi").submit(function()
	{
		
		event.preventDefault();
		$.post("/egrafi2", $("#frmegrafi").serialize(),function(res)
		{
			
			
			if(res.done=="false")
			{
				console.log(res);
				$("#btnhide").hide();
				$("#msg").html(`<button type="submit" id="btn2" class="btn2">Email exists!</button>`);	 
			}

			else
			{
				$("#btnhide").hide();
				$("#msg").html("<div><img style='width: 100px;'src='/uploads/trans_ok1.gif'></div>");
				window.location.href="/syndesi";

			}
			
			
		});
		

	});  // telos formas egrafis
	
	

	// afora tin syndeis tou xristi
	
	$("#frmsyndesi").submit(function()
	{
		event.preventDefault();
		$.post("/syndesi2", $("#frmsyndesi").serialize(),function(res)
		{
			if(res.done=="false")
			{
				$("#msg").html(`
						<div class="alert alert-danger">
						  Invalid credencials
						</div>`);
			}
			else
			{
				window.location.href="/";
			}
		});
	});
	
	
	
	
		// anevasma arxeiou
	
	$("#frmaddcontent").submit(function()
	{
		
		event.preventDefault();
		var formData = new FormData();
		
		var files=$("#filename")[0].files
		formData.append("filename", files[0]);
		formData.append("title", $("#title").val());

		$.ajax({

			url: "/uploadfile",
		    type: "POST",
			success: function (res) {
				
				if(res.done=="false")
				{
					$("#msg").html(`
							<div class="alert alert-danger">
							  Δεν φορτώθηκε το αρχείο !
							</div>`);
				}
				else
				{
					$("#msg").html(`
							<div class="alert alert-success">
							  Το αρχείο φορτώθηκε
							</div>`);
							
							getmycontents();
				}
				
				
			
			},
			async: true,
			data: formData,
			cache: false,
			contentType: false,
			processData: false
		
		});
		

	});
	
	
	
	
   
	
	
	
});

