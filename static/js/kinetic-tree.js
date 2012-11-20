var com;
if(com == undefined){
	com = {};
}

com.nnoco = {};
com.nnoco.Util = {};

com.nnoco.Util.convertNumRefToUnicodeCodePoints = function(str, base){
	var regex = /&#(\d*);/g;
	return str.replace(regex, function(match){
		return String.fromCharCode(
				parseInt(match.replace(regex, "$1")));
	});
	
}

/**
 * Drawing Library(Kinetic.js)와 Tree의 의존성을 제거하기 위하여
 * 트리 노드의 위치와 가중치 정보를 가지는 PositionedTree 객체를 이용한다. 
 */
function PositionedTree(config){
	this.config = config;
	this.rootPos = {
			x : config.rootX,
			y : config.rootY,
	}
	this.gap = {
			x : config.gapX,
			y : config.gapY,
	}
	
	
	this.map = config.map;
	this.root = config.root;
	this.nodes = [];
	
	
};

PositionedTree.prototype = {
	init : function(data){
		
	}
};


PositionedTree.Node = function(obj){
	this.id = obj.id;
	this.parent = obj.parent;
	this.weight = 1;
	this.children = [];
	this.level = 0;
	
	this.data = obj.data;
}

/**
 * PositionedTree 객체의 위치 정보를 받아 Kinetic Library를 이용하여
 * 트리를 시각화 할 수 있도록 하는 어댑터 객체
 * @param pt PositionedTree
 */
function TreeToKineticAdapter(pt){
	this.stage;
	this.layer;
	this.lineLayer;
	this.branchRadius = obj.branchRadius;
}

/**
 * json 데이터와 PositionedTree 연결 어댑터
 *
 */
function PositionedTreeAdapter(data){

}



function VisualTree(obj){
	this.rootY = obj.rootY;
	this.gapX = obj.gapX;
	this.gapY = obj.gapY;
	this.branchRadius = obj.branchRadius;
	this.map = obj.map;
	this.root = obj.root;
	this.stage;
	this.layer;
	this.lineLayer;
	this.branches;
}

Map = function(){
 this.map = new Object();
};   
Map.prototype = {   
    put : function(key, value){   
        this.map[key] = value;
    },   
    get : function(key){   
        return this.map[key];
    },
    containsKey : function(key){    
     return key in this.map;
    },
    containsValue : function(value){    
     for(var prop in this.map){
      if(this.map[prop] == value) return true;
     }
     return false;
    },
    isEmpty : function(key){    
     return (this.size() == 0);
    },
    clear : function(){   
     for(var prop in this.map){
      delete this.map[prop];
     }
    },
    remove : function(key){    
     delete this.map[key];
    },
    keys : function(){   
        var keys = new Array();   
        for(var prop in this.map){   
            keys.push(prop);
        }   
        return keys;
    },
    values : function(){   
     var values = new Array();   
        for(var prop in this.map){   
         values.push(this.map[prop]);
        }   
        return values;
    },
    size : function(){
      var count = 0;
      for (var prop in this.map) {
        count++;
      }
      return count;
    }
};

function jsonAdapter(o){
	/*
	 * id : bid
	 * parent : pid
	 * score : point
	 * .. : uid // 유저아이디?
	 */
	
	return {id : o.bid, parent : o.pid, score : o.point};
}

Branch = function(obj) {
	this.id = obj.id;
	this.parent = obj.parent;
	this.score = obj.score;
	this.level;
	this.weight = 1;
	this.children = [];
};

Branch.prototype = {
	add : function(child){
		this.children.push(child);
	},
}

function createTree(rawBranches){
	var map = new Map();
	var branch;
	var root;
	for(var i=0; i<rawBranches.length ; i++){
		branch = new Branch(jsonAdapter(rawBranches[i]));
		
		if(i==0) root = branch;

		// 부모노드에 추가.
		map.put(branch.id, branch);

		if(branch.parent != 0){ // 0은 루트노드를 의미함.. magic number 제거해야함
			map.get(branch.parent).children.push(branch);
		}
	}

	return {map : map, root : root};
}

// 재귀적 트리 순회
function initTree(branch, lv){
	branch.level = lv;
	console.log(branch);
	switch(branch.children.length){
		case 1:
			branch.weight = initTree(branch.children[0], lv+1);
		break;
		default:
			for(var i = 0 ; i < branch.children.length ; i++){
			branch.weight +=
				initTree(branch.children[i], lv+1);
			}
	}

	//console.log(branch.id + " :: " + (branch.weight < 3 ? 1 : branch.weight));
	return branch.weight < 3 ? 1 : branch.weight;
}

function valueCheck(map){
	var values = map.map;
	for(var i=1 ; i <= values.length ;i++){
		console.log(values[i].id + "::" + values[i].weight);
	}
}

// 시작 초기화
//var map = createTree(book_index);
//var root = map.get(1);
//initTree(root, 0);



function drawTree(root, map){
	var height = 50;
	var radius = 15;
	var vt = new VisualTree({
		rootY : 50,
		gapX : 100,
		gapY : 100,
		branchRadius : 35,
		map : map,
		root : root		
	});

	var $container = $("#container");
	var stage = new Kinetic.Stage({
		container: 'container',
		width : $container.width(),
		height : $container.height(),
		id:"stage",
		fill : "white",
		draggable : true,
	});

	var layer = new Kinetic.Layer();
	var lineLayer = new Kinetic.Layer();

	vt.stage = stage;
	vt.layer = layer;
	vt.lineLayer = lineLayer;

	// 루트 그리기

	// 자식 요소들 그리기
	drawChildren(vt,
		vt.root, stage.getWidth() / 2,
		vt.rootY);

	var treeContainer =new Kinetic.Layer({draggable:true});
	var treeGroup = new Kinetic.Group({draggable:true});

	treeGroup.add(lineLayer);
	treeGroup.add(layer);
	treeContainer.add(treeGroup);
	stage.add(lineLayer);
	stage.add(layer);
	stage.add(treeContainer);
}

function loadImages(sources, callback) {
    var images = {};
    var loadedImages = 0;
    var numImages = 0;
    // get num of sources
    for(var src in sources) {
      numImages++;
    }
    for(var src in sources) {
      images[src] = new Image();
      images[src].onload = function() {
        if(++loadedImages >= numImages) {
          callback(images);
        }
      };
      images[src].src = sources[src];
    }
  }

function drawChildren(vt, branch, x, y){ // vt : visualTree
	var children = branch.children;
	var baseX = x;
	var baseY = y;
	var width = branch.weight * vt.gapX;

	width = 0;
	for(var i = 0 ; i< branch.children.length ; i++){
		width += children[i].weight;
	}

	width *= vt.gapX;

/*	var ox = profileImgs.width * (-0.5);
	var oy = profileImgs.height * (-0.5);*/
	
	// 현재 브랜치를 그림
	var current = new Kinetic.Circle({
		x : x,
		y : y,
		radius : vt.branchRadius,
		 fill : '#2E9AFE',
	});
	current.setShadow({
		color : '#1B5B97',
		blur : 30,
		offset: [0, 0],
		alpha: 0.7,
	});

	current.on('click touchstart', function(evt){
			$(".dialog-container").fadeIn("fast");
			
			$("#dialog-iframe").attr('src', '/posts/get_branchinfo/' + branch.id);
			
			/*$(".dialog").text("ID : " + branch.id + "\n"

				);
			
			$(".dialog").append($("<br><a href='/posts/read_branch/" + branch.id + "'>읽기</a>"));
			
			$(".dialog").append($("<br><a href='/posts/write_branch/" + book_id + "/" + branch.id + "/0'>이어쓰기</a>"));*/
			
			
		});

	vt.layer.add(current);

	x -= width / 2;
	y += vt.gapY;
	
	for(var i = 0 ; i < children.length ; i++){
		//sumOfWeight += children[i].weight;
		drawChildren(vt, children[i],
			x + ((children[i].weight * vt.gapX)/2), y);

		vt.lineLayer.add(new Kinetic.Line({
			points: [baseX, baseY+vt.branchRadius, x + ((children[i].weight * vt.gapX)/2), y],
			stroke : "gray",
			strokeWidth : 1,
		}));


		x += (children[i].weight * vt.gapX);
	}
}

//drawTree(root);