import re
# remove noise & cleans

class PreprocessorService:

    @staticmethod
    def clean(text: str) -> str:
        if not text:
            return ""

        # Remove image placeholders as we are interested in text 
        text = re.sub(
            r"\[image:.*?\]",
            "",
            text,
            flags=re.IGNORECASE,
        )

        # Remove URLs as they add little semantic meaning
        text = re.sub(
            r"https?://\S+",
            "",
            text,
        )

        # Remove empty parentheses
        text = re.sub(
            r"\(\s*\)",
            "",
            text,
        )

        # Remove lines containing only brackets
        text = re.sub(
            r"^[()<>]+$",
            "",
            text,
            flags=re.MULTILINE,
        )

        # Remove invisible Unicode characters like zero width space
        text = re.sub(
            r"[\u00AD\u2007\u200B-\u200F\u2060\uFEFF]",
            "",
            text,
        )

        # Remove everything after common footer markers
        footer_markers = [
            "Sent by",
            "Unsubscribe",
            "Privacy Policy",
            "Terms of Service",
            "You received this email",
            "All rights reserved",
            "Copyright",
            "Manage preferences",
            "View in browser",
        ]

        lower_text = text.lower() 

        for marker in footer_markers:
            idx = lower_text.find(marker.lower())
            if idx != -1:
                text = text[:idx]
                break

        # Remove noisy footer lines that may remain
        footer_keywords = [
            "unsubscribe",
            "privacy policy",
            "terms of service",
            "help center",
            "manage preferences",
            "view in browser",
            "copyright",
            "all rights reserved",
        ]

        cleaned_lines = []

        for line in text.splitlines():

            line = line.strip()

            if not line:
                continue

            lower = line.lower()

            if any(keyword in lower for keyword in footer_keywords):
                continue

            cleaned_lines.append(line)

        text = "\n".join(cleaned_lines)

        # Collapse multiple blank lines
        text = re.sub(
            r"\n{2,}",
            "\n\n",
            text,
        )

        # Collapse multiple spaces/tabs
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        return text.strip()