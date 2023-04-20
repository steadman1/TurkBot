from qbittorrent import Client
import os

class QBittorrent:
    def __init__(self, added_on, amount_left, auto_tmm, availability, category, completed, completion_on, content_path, dl_limit, dlspeed, download_path, downloaded, downloaded_session, eta, f_l_piece_prio, force_start, hash, infohash_v1, infohash_v2, last_activity, magnet_uri, max_ratio, max_seeding_time, name, num_complete, num_incomplete, num_leechs, num_seeds, priority, progress, ratio, ratio_limit, save_path, seeding_time, seeding_time_limit, seen_complete, seq_dl, size, state, super_seeding, tags, time_active, total_size, tracker, trackers_count, up_limit, uploaded, uploaded_session, upspeed):
        self.added_on = added_on
        self.amount_left = amount_left
        self.auto_tmm = auto_tmm
        self.availability = availability
        self.category = category
        self.completed = completed
        self.completion_on = completion_on
        self.content_path = content_path
        self.dl_limit = dl_limit
        self.dlspeed = dlspeed
        self.download_path = download_path
        self.downloaded = downloaded
        self.downloaded_session = downloaded_session
        self.eta = eta
        self.f_l_piece_prio = f_l_piece_prio
        self.force_start = force_start
        self.hash = hash
        self.infohash_v1 = infohash_v1
        self.infohash_v2 = infohash_v2
        self.last_activity = last_activity
        self.magnet_uri = magnet_uri
        self.max_ratio = max_ratio
        self.max_seeding_time = max_seeding_time
        self.name = name
        self.num_complete = num_complete
        self.num_incomplete = num_incomplete
        self.num_leechs = num_leechs
        self.num_seeds = num_seeds
        self.priority = priority
        self.progress = round(progress * 100, 2)
        self.ratio = ratio
        self.ratio_limit = ratio_limit
        self.save_path = save_path
        self.seeding_time = seeding_time
        self.seeding_time_limit = seeding_time_limit
        self.seen_complete = seen_complete
        self.seq_dl = seq_dl
        self.size = size
        self.state = state
        self.super_seeding = super_seeding
        self.tags = tags
        self.time_active = time_active
        self.total_size = total_size
        self.tracker = tracker
        self.trackers_count = trackers_count
        self.up_limit = up_limit
        self.uploaded = uploaded
        self.uploaded_session = uploaded_session
        self.upspeed = upspeed

class PyTorrent:
    def __init__(self, category):
        try:
            self.qb = Client('http://127.0.0.1:8080/')
            self.qb.login('admin', 'root420')
        except ConnectionError:
            print("Please open the qBittorrent App and start qbittorrent server in the Tools > Options > Web UI Interface (remote control).")
        self.category = category

    def download(self, torrent_id):
        """
        Download a torrent file
        
        params:
        torrent_id can be:
            * magnet uri
            * http url to .torrent file
            * filesystem path to .torrent file
            * info hash (hex string)
        """
        save_path = "F:\Movies" # os.path.join(os.path.dirname(__file__), "movies")
        self.qb.download_from_link(torrent_id, savepath=save_path, category=self.category)

    def cancel(self, torrent_id):
        """Cancel a torrent download and delete all related data"""
        self.qb.delete_permanently(torrent_id)

    def status(self, results_count=5):
        return [QBittorrent(**torrent) for torrent in self.qb.torrents(category=self.category)[:results_count]]