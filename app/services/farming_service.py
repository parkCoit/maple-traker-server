from datetime import datetime

from app.core.supabase import supabase


class FarmingService:

    @staticmethod
    def get_logs(nickname: str):
        return supabase.table("logs") \
            .select("*") \
            .eq("nickname", nickname) \
            .execute().data

    @staticmethod
    def create_log(data: dict):
        return supabase.table("logs") \
            .insert(data) \
            .execute().data

    @staticmethod
    def build_farming_summary(farming: list[dict]) -> dict:
        now = datetime.now()

        today_str = now.strftime("%Y-%m-%d")

        today_total = 0
        week_total = 0
        month_total = 0

        current_week = now.isocalendar()[1]
        for log in farming:
            # server stores meso_man, f_price, g_price in 'man' units (10,000)
            # convert to raw meso (units) for client consumption
            meso_man = log.get("meso_man") or 0
            f_price = log.get("f_price") or 0
            g_price = log.get("g_price") or 0
            frags = log.get("frags") or 0
            gems = log.get("gems") or 0

            # coerce numeric-like values to floats safely
            try:
                meso_man = float(meso_man)
            except Exception:
                meso_man = 0
            try:
                f_price = float(f_price)
            except Exception:
                f_price = 0
            try:
                g_price = float(g_price)
            except Exception:
                g_price = 0
            try:
                frags = float(frags)
            except Exception:
                frags = 0
            try:
                gems = float(gems)
            except Exception:
                gems = 0

            total_man = meso_man + frags * f_price + gems * g_price
            total_meso_raw = int(total_man)
            meso_raw = int(meso_man)

            # attach raw values to the log
            log["total_meso"] = total_meso_raw
            log["meso"] = meso_raw

            date_str = log.get("date")
            if not date_str:
                continue
            try:
                log_date = datetime.strptime(date_str, "%Y-%m-%d")
            except Exception:
                continue

            if date_str == today_str:
                today_total += total_meso_raw

            if log_date.year == now.year and log_date.month == now.month:
                month_total += total_meso_raw

            if log_date.isocalendar()[1] == current_week:
                week_total += total_meso_raw

        return {
            "today_total": today_total,
            "week_total": week_total,
            "month_total": month_total,
        }