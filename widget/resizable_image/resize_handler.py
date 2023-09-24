from widget.aspect_frame import AspectFrame, AfterResizingEvent

img_resize_threshold = 5


def frm_resize_handler(e: AfterResizingEvent):
    assert isinstance(e.widget, AspectFrame)
    asp_frm = e.widget
    cell = asp_frm.wfc_cell
    new_cell_size = min(e.new_w, e.new_h)
    new_img_size = int(new_cell_size / cell.max_side)

    if abs(new_img_size - cell.img_size) > img_resize_threshold:
        for other_frm in [w for w in asp_frm.master.grid_slaves() if isinstance(w, AspectFrame)]:
            if cell.max_side == other_frm.wfc_cell.max_side:
                other_frm.set_image_size(new_img_size)
