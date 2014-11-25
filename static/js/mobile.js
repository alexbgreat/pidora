
	function getStations(index)
	{
		$.get("api", {json:JSON.stringify({"method":"GetStationData", "id":1})}).done(update_stationlist);
	}

	function update_stationlist(stationList)
		{
			stationList = stationList.stationData;
			for(var i = 0; i < stationList.stations.length; i++)
			{
				$('select[name=stationselect]')
					.append($('<option>', { value : i.toString() }).text(stationList.stations[i]));
			}
			window.setTimeout(update_song(), 1000);
		}

	function explainSong()
	{
		switch(1)
		{
			case 1:
				$.get("api", {json:JSON.stringify({"method":"GetExplanation", "id":1})}).done(function(explain)
				{
					alert(explain.explanation);
				});
				break;
			case 2:
				alert("How can you expect an explanation when there's nothing playing? You're being silly.");
				break;
			case 3:
				alert("There does not exist an appropriate explanation for this track. Sorry about that.");
				break;
		}
	}
		getStations(0);


	function update_song(){
		$.ajax({
			url:'/api',
			data:'json='+encodeURIComponent('{"method":"GetSongInfo","id":1}'),
			method:"get",
			dataType:"json",
			success:function(data){
				var title = data.song.title
				if(data.song.loved){
					title = title + " <3"
				}
				$("#title").text(title);
				$("#artist").text(data.song.artist);
				$("#album").text(data.song.album);
				$("#albumart").attr("src",data.song.artURL);
				$('select').val($("option:contains('"+data.song.station_name+"')").val()).selectmenu('refresh');
			}
		});
	}
	jQuery(document).ready(function () {
	setInterval('update_song()', 5000);

  $(".btn").live('click', function() {
      this.src = this.src.replace("_off","_on");
      setTimeout(function(t){
      	t.src = t.src.replace("_on","_off")},400,this);
      setTimeout(update_song(),1000);
  })


	$('select[name=stationselect]').change(function()
{
	var id = $('select[name=stationselect]').val();
	$.get("api", {json:JSON.stringify({"method":"ChangeStation", "id":1, "stationID":id})}).done(function()
		{
			window.setTimeout(update_song(), 1000);
		});
});


	});


