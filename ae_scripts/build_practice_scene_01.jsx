/*
  build_practice_scene_01.jsx — The Engineering Atlas
  Builds your first practice scene from the asset library, fully assembled:

    comp "practice_01_establishing"  (3840x2160, 30fps, 12s)
      - parchment background solid (#F5F0E8)
      - fort tower (right), banyan tree (left), rocks (foreground)
      - two clouds drifting slowly right (far one slower = depth)
      - a CAMERA_CTRL null: everything parented to it, scale 100% -> 105%
        over 12s with Easy Ease  (the "Rung 1" push-in)

  Run it in After Effects:  File > Scripts > Run Script File…  and pick this file.
  Everything arrives as ONE undo step (Cmd+Z removes it all).

  NOTE for reading this code: AE scripting is ExtendScript — an OLD dialect of
  JavaScript (ES3). No let/const, no arrow functions, no template strings.
*/

(function () {

    // ---------- helpers ----------

    function repoRoot() {
        // this file lives in <repo>/ae_scripts/, so the repo is one level up
        var here = new File($.fileName).parent;
        var root = here.parent;
        if (Folder(root.fsName + "/assets_library").exists) return root;
        // moved the script? just point AE at the repo folder instead
        return Folder.selectDialog("Select the repo folder (the one containing assets_library)");
    }

    function importPng(project, bin, path) {
        var f = new File(path);
        if (!f.exists) throw new Error("Missing asset: " + path);
        var item = project.importFile(new ImportOptions(f));
        item.parentFolder = bin;
        return item;
    }

    // scale a layer so its rendered height = targetH pixels
    function addScaled(comp, item, targetH, name) {
        var layer = comp.layers.add(item);
        var s = (targetH / item.height) * 100;
        var prop = layer.transform.scale;
        var v = prop.value, out = [], i;
        for (i = 0; i < v.length; i++) out.push(s);
        prop.setValue(out);
        layer.name = name;
        return layer;
    }

    // place by bottom-center: element "stands" on groundY
    function standAt(layer, x, groundY, renderedH) {
        layer.transform.position.setValue([x, groundY - renderedH / 2]);
    }

    // straight horizontal drift: +dx pixels over the comp duration (linear is fine for clouds)
    function drift(layer, dx, duration) {
        var p = layer.transform.position;
        var v = p.value;
        p.setValueAtTime(0, v);
        p.setValueAtTime(duration, [v[0] + dx, v[1]]);
    }

    // apply Easy Ease (speed 0, influence 33%) to every keyframe of a property
    function easeAllKeys(prop) {
        var e = new KeyframeEase(0, 33.33);
        var v = prop.value, arr = [], i, k;
        var dims = (v && v.length) ? v.length : 1;
        for (i = 0; i < dims; i++) arr.push(e);
        for (k = 1; k <= prop.numKeys; k++) {
            try { prop.setTemporalEaseAtKey(k, arr, arr); }
            catch (err) { prop.setTemporalEaseAtKey(k, [e], [e]); }  // spatial props take 1
        }
    }

    // ---------- build ----------

    app.beginUndoGroup("Build practice_01_establishing");
    try {
        var root = repoRoot();
        if (!root) throw new Error("No repo folder selected.");
        var lib = root.fsName + "/assets_library";

        var proj = app.project || app.newProject();
        var bin = proj.items.addFolder("assets_library");

        var W = 3840, H = 2160, FPS = 30, DUR = 12;
        var comp = proj.items.addComp("practice_01_establishing", W, H, 1.0, DUR, FPS);
        comp.bgColor = [0.961, 0.941, 0.910];

        // background: brand parchment #F5F0E8 (not parented — a flat color has no parallax)
        comp.layers.addSolid([0.961, 0.941, 0.910], "parchment_bg", W, H, 1.0, DUR);

        var cloudItem = importPng(proj, bin, lib + "/nature/cloud_01.png");
        var towerItem = importPng(proj, bin, lib + "/architecture/fort_tower_01.png");
        var treeItem  = importPng(proj, bin, lib + "/nature/tree_banyan_01.png");
        var rocksItem = importPng(proj, bin, lib + "/nature/rocks_01.png");

        // far cloud first so it stacks BEHIND the near one (each add lands on top)
        var cloudFar = addScaled(comp, cloudItem, 240, "cloud_far");
        cloudFar.transform.position.setValue([2950, 330]);
        cloudFar.transform.opacity.setValue(80);

        var cloudNear = addScaled(comp, cloudItem, 400, "cloud_near");
        cloudNear.transform.position.setValue([950, 460]);

        var tower = addScaled(comp, towerItem, 1150, "fort_tower");
        standAt(tower, 2550, 1900, 1150);

        var tree = addScaled(comp, treeItem, 980, "banyan_tree");
        standAt(tree, 1000, 1890, 980);

        var rocks = addScaled(comp, rocksItem, 260, "rocks_fg");
        standAt(rocks, 1800, 2020, 260);

        // motion 1 — clouds drift right; far cloud slower = instant depth
        drift(cloudNear, 240, DUR);
        drift(cloudFar, 130, DUR);

        // motion 2 — the push-in. A null at comp center; anchor == position makes its
        // transform identity, so parenting causes no jump and scaling pivots on center.
        var cam = comp.layers.addNull(DUR);
        cam.name = "CAMERA_CTRL (scale = push-in)";
        cam.transform.anchorPoint.setValue([W / 2, H / 2]);
        cam.transform.position.setValue([W / 2, H / 2]);

        var kids = [cloudFar, cloudNear, tower, tree, rocks], i;
        for (i = 0; i < kids.length; i++) kids[i].parent = cam;

        var sp = cam.transform.scale;
        var s0 = sp.value, sEnd = [], j;
        for (j = 0; j < s0.length; j++) sEnd.push(s0[j] * 1.05);
        sp.setValueAtTime(0, s0);
        sp.setValueAtTime(DUR, sEnd);
        easeAllKeys(sp);            // <-- THE craft move: eased, never linear, camera motion

        comp.openInViewer();
        alert("Built 'practice_01_establishing'.\n\nPress SPACE to preview.\n" +
              "Try changing: the 1.05 push amount, cloud drift 240px, or drag elements around.\n" +
              "One Cmd+Z removes the whole thing.");
    } catch (err) {
        alert("Script stopped: " + err.message);
    } finally {
        app.endUndoGroup();
    }

})();
