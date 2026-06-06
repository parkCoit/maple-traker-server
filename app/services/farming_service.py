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
            total_meso = (
                log["meso_man"]
                + log["frags"] * log.get("f_price", 0)
                + log["gems"] * log.get("g_price", 0)
            )

            log["total_meso"] = total_meso

            log_date = datetime.strptime(log["date"], "%Y-%m-%d")

            if log["date"] == today_str:
                today_total += total_meso

            if (
                log_date.year == now.year
                and log_date.month == now.month
            ):
                month_total += total_meso

            if log_date.isocalendar()[1] == current_week:
                week_total += total_meso

        return {
            "today_total": today_total,
            "week_total": week_total,
            "month_total": month_total,
        }