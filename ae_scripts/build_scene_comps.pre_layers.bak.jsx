/*
  build_scene_comps.jsx — The Engineering Atlas · video 001 (Roman Aqueduct)
  Studio pass-7 scaffold (ae-director). Builds one 4K comp per scriptable scene:
    - comp "scene_NN"  (3840x2160, 30fps, duration = scene + 1s handles each end)
    - the plate imported, scaled to COVER the frame, centered
    - a CAMERA_CTRL null; the plate parented to it
    - the board's camera move as EASED keyframes:
        push_in  -> null scale base -> base*(1+amt%)
        pull_back-> null scale base*(1+amt%) -> base   (reveal)
        pan_*    -> plate at ~115% cover, null position keyed the pan distance
      keys sit inside 1s handles with the board's hold_in / hold_out.
  Only fam_plate_push + fam_map_route scenes are here; assembly, and the masked-waterline
  cutaways, are hand-built (see ae_build.jsx=null in the board).

  Run:  File > Scripts > Run Script File…  -> pick this file.  ONE undo step.
  ExtendScript = ES3: no let/const, no arrows, no template strings.
*/
(function () {
    var W = 3840, H = 2160, FPS = 30, HANDLES = 1.0;
    var PROJECT_SUBDIR = "projects/001_roman_aqueduct";

    var SCENES = [
  {id:"scene_00", plate:"images/scene_00.png", dur:26.9, move:"push_in", amt:5, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_02", plate:"images/scene_02.png", dur:12.0, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_07", plate:"images/scene_07.png", dur:9.4, move:"pan_right", amt:0, panpx:55, hin:0.8, hout:0.8},
  {id:"scene_09", plate:"images/scene_09.png", dur:13.1, move:"pull_back", amt:8, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_10", plate:"images/scene_10.png", dur:7.7, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_11", plate:"images/scene_11.png", dur:3.0, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_12", plate:"images/scene_12.png", dur:7.2, move:"pan_right", amt:0, panpx:55, hin:0.8, hout:0.8},
  {id:"scene_13", plate:"images/scene_13.png", dur:12.1, move:"pan_right", amt:0, panpx:55, hin:0.8, hout:0.8},
  {id:"scene_14", plate:"images/scene_14.png", dur:8.7, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_15", plate:"images/scene_15.png", dur:13.1, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_16", plate:"images/scene_16.png", dur:7.9, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_17", plate:"images/scene_17.png", dur:11.4, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_18", plate:"images/scene_18.png", dur:7.9, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_20", plate:"images/scene_20.png", dur:9.8, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_21", plate:"images/scene_21.png", dur:9.4, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_22", plate:"images/scene_22.png", dur:8.2, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_23", plate:"images/scene_23.png", dur:9.8, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_24", plate:"images/scene_24.png", dur:8.9, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_25", plate:"images/scene_25.png", dur:4.9, move:"push_in", amt:5, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_26", plate:"images/scene_26.png", dur:10.5, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_27", plate:"images/scene_27.png", dur:10.8, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_28", plate:"images/scene_28.png", dur:14.0, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_29", plate:"images/scene_29.png", dur:7.8, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_30", plate:"images/scene_30.png", dur:9.9, move:"pan_right", amt:0, panpx:55, hin:0.8, hout:0.8},
  {id:"scene_31", plate:"images/scene_31.png", dur:11.4, move:"pan_right", amt:0, panpx:55, hin:0.8, hout:0.8},
  {id:"scene_32", plate:"images/scene_32.png", dur:3.0, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_33", plate:"images/scene_33.png", dur:9.9, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_34", plate:"images/scene_34.png", dur:11.9, move:"pull_back", amt:8, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_36", plate:"images/scene_36.png", dur:9.6, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_37", plate:"images/scene_37.png", dur:7.5, move:"pan_right", amt:0, panpx:55, hin:0.8, hout:0.8},
  {id:"scene_38", plate:"images/scene_38.png", dur:8.0, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_39", plate:"images/scene_39.png", dur:9.4, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_40", plate:"images/scene_40.png", dur:5.7, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_41", plate:"images/scene_41.png", dur:7.1, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_42", plate:"images/scene_42.png", dur:5.5, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_43", plate:"images/scene_43.png", dur:12.8, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_44", plate:"images/scene_44.png", dur:4.1, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_45", plate:"images/scene_45.png", dur:11.1, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_46", plate:"images/scene_46.png", dur:8.5, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_47", plate:"images/scene_47.png", dur:11.0, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_48", plate:"images/scene_48.png", dur:8.3, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_49", plate:"images/scene_49.png", dur:14.1, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_50", plate:"images/scene_50.png", dur:13.1, move:"pan_right", amt:0, panpx:55, hin:0.8, hout:0.8},
  {id:"scene_51", plate:"images/scene_51.png", dur:12.3, move:"push_in", amt:5, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_52", plate:"images/scene_52.png", dur:6.8, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_53", plate:"images/scene_53.png", dur:14.5, move:"pull_back", amt:8, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_54", plate:"images/scene_54.png", dur:13.6, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_55", plate:"images/scene_55.png", dur:8.8, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_56", plate:"images/scene_56.png", dur:10.3, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_57", plate:"images/scene_57.png", dur:8.9, move:"push_in", amt:5, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_58", plate:"images/scene_58.png", dur:9.7, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_59", plate:"images/scene_59.png", dur:14.5, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_60", plate:"images/scene_60.png", dur:3.0, move:"pan_right", amt:0, panpx:55, hin:0.8, hout:0.8},
  {id:"scene_61", plate:"images/scene_61.png", dur:7.8, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_62", plate:"images/scene_62.png", dur:10.2, move:"push_in", amt:4, panpx:0, hin:0.9, hout:0.9},
  {id:"scene_63", plate:"images/scene_63.png", dur:7.5, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8},
  {id:"scene_64", plate:"images/scene_64.png", dur:7.8, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_68", plate:"images/scene_68.png", dur:7.8, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_69", plate:"images/scene_69.png", dur:9.5, move:"push_in", amt:5, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_70", plate:"images/scene_70.png", dur:10.4, move:"push_in", amt:5, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_71", plate:"images/scene_71.png", dur:10.9, move:"push_in", amt:6, panpx:0, hin:0.7, hout:0.7},
  {id:"scene_72", plate:"images/scene_72.png", dur:5.4, move:"push_in", amt:4, panpx:0, hin:0.8, hout:0.8}
    ];

    function repoRoot() {
        var here = new File($.fileName).parent, root = here.parent;
        if (Folder(root.fsName + "/assets_library").exists) return root;
        return Folder.selectDialog("Select the repo folder (the one containing assets_library)");
    }
    function importPng(project, bin, path) {
        var f = new File(path);
        if (!f.exists) throw new Error("Missing plate: " + path);
        var item = project.importFile(new ImportOptions(f));
        item.parentFolder = bin; return item;
    }
    function coverScale(item) { return Math.max(W / item.width, H / item.height) * 100; }
    function easeAll(prop) {
        var e = new KeyframeEase(0, 40), arr = [], i, k, dims = 2;
        try { dims = prop.value.length; } catch (er) { dims = 1; }
        for (i = 0; i < dims; i++) arr.push(e);
        for (k = 1; k <= prop.numKeys; k++) {
            try { prop.setTemporalEaseAtKey(k, arr, arr); }
            catch (err) { prop.setTemporalEaseAtKey(k, [e], [e]); }
        }
    }

    app.beginUndoGroup("Build all scene comps (001)");
    try {
        var root = repoRoot(); if (!root) throw new Error("No repo folder selected.");
        var base = root.fsName + "/" + PROJECT_SUBDIR;
        var proj = app.project || app.newProject();
        var bin = proj.items.addFolder("plates_001");
        var built = 0, s, i;

        for (i = 0; i < SCENES.length; i++) {
            s = SCENES[i];
            var compDur = s.dur + 2 * HANDLES;
            var comp = proj.items.addComp(s.id, W, H, 1.0, compDur, FPS);
            comp.bgColor = [0.961, 0.941, 0.910];              // brand parchment
            comp.layers.addSolid([0.961, 0.941, 0.910], "parchment_bg", W, H, 1.0, compDur);

            var item = importPng(proj, bin, base + "/" + s.plate);
            var plate = comp.layers.add(item);
            var isPan = (s.move.substring(0, 3) === "pan");
            var cov = coverScale(item) * (isPan ? 1.15 : 1.0);  // pan needs overflow room
            plate.transform.scale.setValue([cov, cov]);
            plate.transform.position.setValue([W / 2, H / 2]);
            plate.name = "plate";

            var cam = comp.layers.addNull(compDur);
            cam.name = "CAMERA_CTRL";
            cam.transform.anchorPoint.setValue([W / 2, H / 2]);
            cam.transform.position.setValue([W / 2, H / 2]);
            plate.parent = cam;

            var t0 = s.hin, t1 = compDur - s.hout;              // move sits inside the holds/handles
            if (s.move === "push_in" || s.move === "pull_back") {
                var sp = cam.transform.scale, b = sp.value, k = 1 + s.amt / 100.0;
                var lo = [b[0], b[1]], hi = [b[0] * k, b[1] * k];
                if (s.move === "push_in") { sp.setValueAtTime(t0, lo); sp.setValueAtTime(t1, hi); }
                else { sp.setValueAtTime(t0, hi); sp.setValueAtTime(t1, lo); }
                easeAll(sp);
            } else if (isPan) {
                var pp = cam.transform.position, c = pp.value;
                var dist = s.panpx * s.dur;                     // total pan px over the read
                var dir = (s.move === "pan_left") ? 1 : (s.move === "pan_right") ? -1 : 0;
                // pan_right = world slides left = null moves right; clamp to the 15% overflow
                var maxpx = (cov / 100 * item.width - W) / 2; if (dist / 2 > maxpx) dist = maxpx * 2;
                pp.setValueAtTime(t0, [c[0] - dir * dist / 2, c[1]]);
                pp.setValueAtTime(t1, [c[0] + dir * dist / 2, c[1]]);
                easeAll(pp);
            }
            built++;
        }
        alert("Built " + built + " scene comps (fam_plate_push + fam_map_route).\n" +
              "Each: plate imported, CAMERA_CTRL rigged, eased move keys set.\n" +
              "Next by hand: holds/taste, parallax layers, the 10 assembly + 2 waterline scenes.\n" +
              "One Cmd+Z removes everything.");
    } catch (err) {
        alert("Script stopped: " + err.message);
    } finally {
        app.endUndoGroup();
    }
})();
