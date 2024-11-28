import maya.plugin.timeSliderBookmark.timeSliderBookmark as maya_tsb
import pymel.core as pm
from dataclasses import dataclass
import json, os

@dataclass
class TimelineBookmark:
    node: str
    name: str
    start: int
    stop: int
    color: [float, float, float]

    def create_maya_node(self, update_existing=False, force=False):
        if pm.objExists(self.node):
            bm_node = pm.PyNode(self.node)
            if update_existing:
                pm.setAttr(bm_node.name, self.name),
                pm.setAttr(bm_node.timeRangeStart, self.start),
                pm.setAttr(bm_node.timeRangeStop, self.stop),
                pm.setAttr(bm_node.color, self.color, type="float3")
            elif force:
                pm.delete(bm_node)
                new_bm_node = self.node = maya_tsb.createBookmark(name=self.name, start=self.start, stop=self.stop, color=self.color)
                pm.rename(new_bm_node, self.node)
                bm_node = new_bm_node
            else:
                pm.warning(f"TimelineBookmark {self.node} already exists - skipping creation")
        else:
            self.node = maya_tsb.createBookmark(name=self.name, start=self.start, stop=self.stop, color=self.color)
            bm_node = pm.PyNode(self.node)

        return bm_node

    def frame(self):
        maya_tsb.frameBookmark(self.node)

    def select(self):
        pm.select(self.node)

    def as_dict(self):
        return {
            "node": self.node,
            "name": self.name,
            "start": self.start,
            "stop": self.stop,
            "color": self.color
        }

def get_maya_bookmarks():
    bookmarks = [TimelineBookmark(
                        bm,
                        pm.getAttr(f"{bm}.name"),
                        pm.getAttr(f"{bm}.timeRangeStart"),
                        pm.getAttr(f"{bm}.timeRangeStop"),
                        pm.getAttr(f"{bm}.color")
                    ) for bm in maya_tsb.getAllBookmarks()]
    return bookmarks
                
def split_bookmarks_to_scenes(bookmarks, scene_name="", force=False):
    if not outputname:
        scene_name = os.path.splitext(pm.sceneName())[0]
        scene_ext = ".".join(os.path.splitext(pm.sceneName())[1:])

    for bm in bookmarks:
        bm.frame
        new_name = f"{scene_name}_{bm.name}.{scene_ext}"
        pm.saveAs(new_name, f=force)

    maya_tsb.frameAllBookmark()

def export_bookmarks(bookmarks, export_path=""):
    if not export_path:
        export_path = pm.fileDialog2(dialogStyle=2, caption="Export Scene Bookmarks", fileMode=0, fileFilter="Timeline Bookmark Files - .json (*.json)", okCaption="Save", startingDirectory=os.path.dirname(pm.sceneName()))[0]
        bookmark_data = [bm.as_dict() for bm in bookmarks]

    with open(export_path, 'w') as export_file:
        export_data = json.dumps(bookmark_data, indent=4)
        export_file.write(export_data)

def import_bookmarks(import_paths = "", create_nodes=False, update_existing=True, force_creation=False):
    if not import_paths:
        import_paths = pm.fileDialog2(dialogStyle=2, caption="Import Scene Bookmarks", fileMode=4, fileFilter="Timeline Bookmark Files - .json (*.json)", okCaption="Import", startingDirectory=os.path.dirname(pm.sceneName()))[0]
        
    if type(import_paths) is not list:
        import_paths=[import_paths]

    bookmarks = []
    for import_path in import_paths:
        with open(import_path, 'r') as import_file:
            import_data = json.load(import_file)
            bookmarks.extend([TimelineBookmark(
                                bm.get('node'),
                                bm.get('name'),
                                bm.get('start'),
                                bm.get('stop'),
                                bm.get('color')
                            ) for bm in import_data]
                        )

    if create_nodes:
        for bm in bookmarks:
            bm.create_maya_node(update_existing=update_existing, force=force_creation)
    return bookmarks

        




