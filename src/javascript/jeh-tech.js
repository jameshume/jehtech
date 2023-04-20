/*! JEH-Tech v2.0.0 | (c) 2022 */
function CreatePageContents() {
	try {
		__CreatePageContents();
		__CreateContentsPopup();
	}
	catch (exc) {
		var pageContents = $('#page_contents');	
		if( pageContents.length !== 0 ) {
			pageContents.append(`Failed to generate contents: ${exc}`);
		}
		console.error(exc)
	}
}

function __CreateContentsPopup() {
	let pageContents = $('#page_contents');
	title = $("h1.title");
	if( title.length == 2 ) {
		title = title[1];
		contentsPopup = pageContents.clone();
		contentsPopup.find("a").each(function() {
			$(this).on("click", function(e) {
				contentsPopup.dialog("close");
			});
		});

		contentsPopup.attr("title", "Contents");
		contentsPopup.dialog({
			autoOpen: false,
			resizable: false,
			height: 350,
			show: {
				effect: "blind",
				duration: 1000
			},
			hide: {
				effect: "explode",
				duration: 1000
			}
		});
		newButton = $("<button id='contents_btn'>Contents</button>");
		newButton.click(function() {
			contentsPopup.dialog("open");
		});
		$(title).append(newButton);
	}
}

function __CreatePageContents() {
	// Searching the entire DOM is painfully slow to the extent the browser freezes. Thus search is limited
	// to only those
	const nodes_that_could_contain_headers = ["MAIN", "SECTION", "DIV", "H1", "H2", "H3", "H4", "H5", "H6"]
	const page_contents_div = document.getElementById("page_contents");
	const el_list = [page_contents_div];
	const contents_ul = document.createElement("UL");
	const min_header_level = 2;
	let current_header_level = 2;
	let contents_ul_stack = [contents_ul];
	let toc_idx = 1;

	while(el_list.length > 0) {
		const node = el_list.pop();
		// Check if there are still nodes left in the list
		if (node !== undefined && node !== null) {
			// There is a node left. Add the first sibling of this node that can contain an H[16]
			// tag to the list. It will be visited after any children of this node have been
			// visited.		
			let iter_node = node;
			while (iter_node.nextElementSibling) {
				if (nodes_that_could_contain_headers.find(e => e == iter_node.nextElementSibling.tagName) !== undefined) {
					el_list.push(iter_node.nextElementSibling);
					break;
				}
				iter_node = iter_node.nextElementSibling;
			}

			// Add the first child node that can potentially contain a heading tag to the list.
			iter_node = node;
			while (iter_node.firstElementChild) {
				if (nodes_that_could_contain_headers.find(e => e == iter_node.firstElementChild.tagName) !== undefined) {
					// The node has children. Add the first child to the list.
					el_list.push(iter_node.firstElementChild);
					break;
				}
				iter_node = iter_node.firstElementChild;
			}

			// Visit the current tag
			if (node.tagName.length == 2 && node.tagName.substring(0,1) == "H") {
				if (node.id === '') {
					node.id = `TOC_${toc_idx}`;
					toc_idx += 1;
				}
				const heading_level = parseInt(node.tagName.substring(1,2));
				if (heading_level < min_header_level) {
					throw new Error(`Found an <H${heading_level}> tag, which is not allowed in contents body`)
				}
				else {
					if (heading_level == current_header_level) {						
						const current_contents_ul = contents_ul_stack[contents_ul_stack.length - 1];
						const new_li = document.createElement("LI");
						new_li.innerHTML = `<a href="#${node.id}">${node.innerText}</a>`;
						current_contents_ul.appendChild(new_li);
					}
					else if (heading_level > current_header_level) {
						if ((heading_level - current_header_level) > 1) {
							throw new Error(
								[`A header tag has been skipped. Curent lvl is ${current_header_level}, `,
								 `new lvl is ${heading_level}`
								].join("")
							)
						}
						const current_contents_ul = contents_ul_stack[contents_ul_stack.length - 1];
						const new_ul = document.createElement("UL");
						new_ul.innerHTML = `<li><a href="#${node.id}">${node.innerText}</a></li>`;
						current_contents_ul.appendChild(new_ul);
						contents_ul_stack.push(new_ul);
					}
					else { // (heading_level < current_header_level)
						const num_levels_to_pop = current_header_level - heading_level;
						contents_ul_stack = contents_ul_stack.slice(0, -num_levels_to_pop)
						const current_contents_ul = contents_ul_stack[contents_ul_stack.length - 1];
						const new_li = document.createElement("LI");
						new_li.innerHTML = `<a href="#${node.id}">${node.innerText}</a>`;
						current_contents_ul.appendChild(new_li);
					}

					current_header_level = heading_level;
				}
			}

			page_contents_div.appendChild(contents_ul);
		}
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

	$('#small_text').click(function(){ $('body').css('font-size', '8pt');});
	$('#medium_text').click(function(){ $('body').css('font-size', '10pt');});
	$('#big_text').click(function(){ $('body').css('font-size', '12pt');});

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
