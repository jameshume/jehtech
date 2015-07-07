/*! JEH-Tech v1.0.0 | (c) 2015 */
function CreatePageContents() {
	var pageContents = $('#page_contents');
	if( pageContents ) {
		var liObj = $('<li></li>');
		var olObj = $('<ol></ol>');
		var aObj  = $('<a href=""></a>'); 
		var olRoot = olObj.clone();
		var nextIdx = 0;
		$('h2').each(function() {
			if(nextIdx > 0 ) {
				var nodeText = $(this).text();
				$(this).html('<a id="contents_' + nextIdx.toString() + '">' + nodeText + '</a>');
				
				var newLiObj = liObj.clone();
				var newAObj  = aObj.clone();
				newAObj.prop('href', '#contents_' + nextIdx.toString());
				newAObj.text( nodeText );
				newLiObj.append(newAObj);
				olRoot.append(newLiObj);
				
				var h2SectionDiv = $(this).next();
				if( h2SectionDiv[0].tagName == "DIV" ) {
					var olSubRoot = olObj.clone();
					var subIndex = 0;
					$.each(h2SectionDiv.children("h3"), function() {
						var subNodeText = $(this).text();
						var idString = 'contents_' + nextIdx.toString() + '_' + subIndex.toString();
						$(this).html('<a id="' + idString + '">' + subNodeText + '</a>');
						var newSubLiObj = liObj.clone();
						var newSubAObj  = aObj.clone();
						newSubAObj.prop('href', '#' + idString);
						newSubAObj.text( subNodeText );
						newSubLiObj.append(newSubAObj);
						olSubRoot.append(newSubLiObj);
						++subIndex;
					});
					newLiObj.append(olSubRoot);
				}
			}
			++nextIdx;
		});
		pageContents.append(olRoot);
	}
}

function AddLinkToTeleTypeText(textToReplaceDict) {
	$("tt").each(function() {
		for (var key in textToReplaceDict) {
			if(textToReplaceDict.hasOwnProperty(key)) {
				linkHref = textToReplaceDict[key];
				rePattern = "(\\b" + key + "(\\s*\\(.*\\)){0,1}" + ")";
				reObj = new RegExp(rePattern, 'i');
				$(this).html($(this).html().replace(reObj, '<a target="_blank" href="' + linkHref + '">$1</a>'));
			}
		}
	});
}

$(function(){
	CreatePageContents();

	
	sidebar = $('#sidebar');
	title   = $('#content h1.title');
	mainWin = $(window);

	headerHeight = $('#header').height();

	sidebar.height(mainWin.height());

	$(window).resize(function() {
		sidebar.height(mainWin.height());
	});

	$(window).scroll(function (event) {
		var scroll = mainWin.scrollTop();
		if(scroll >= headerHeight) {
			sidebar.css('top', '0');
			title.css('position', 'fixed');
			title.css('top', '0');
		} else {
			sidebar.css('top', headerHeight-scroll);
			title.css('position', 'relative');
		}
		sidebar.height(mainWin.height());
	});
});
