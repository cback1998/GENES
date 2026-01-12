"""A lightweight terminal-based xiuxian (cultivation) adventure game.

Run with:
    python scripts/xiuxian_game.py
"""
from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List


STAGES: List[str] = [
    "凡人",
    "练气",
    "筑基",
    "金丹",
    "元婴",
    "化神",
    "合体",
    "大乘",
    "飞升",
]


@dataclass
class Player:
    name: str
    stage_index: int = 0
    exp: int = 0
    health: int = 30
    max_health: int = 30
    qi: int = 20
    max_qi: int = 20
    spirit_stones: int = 5
    fame: int = 0
    inventory: Dict[str, int] = field(
        default_factory=lambda: {"灵草": 1, "灵丹": 0, "护心符": 0}
    )

    @property
    def stage(self) -> str:
        return STAGES[self.stage_index]

    def gain_exp(self, amount: int) -> None:
        self.exp += amount
        while self.stage_index < len(STAGES) - 1:
            threshold = (self.stage_index + 1) * 20
            if self.exp >= threshold:
                self.exp -= threshold
                self.stage_index += 1
                self.max_health += 10
                self.health = self.max_health
                self.max_qi += 10
                self.qi = self.max_qi
                print(f"你的境界突破至【{self.stage}】！气血和灵力恢复。\n")
            else:
                break

    def is_alive(self) -> bool:
        return self.health > 0


def describe_player(player: Player) -> None:
    print(
        f"修士：{player.name}\n"
        f"境界：{player.stage}\n"
        f"经验：{player.exp}\n"
        f"声望：{player.fame}\n"
        f"气血：{player.health}/{player.max_health}  灵力：{player.qi}/{player.max_qi}\n"
        f"灵石：{player.spirit_stones}\n"
        f"行囊：{', '.join([f'{k}x{v}' for k, v in player.inventory.items()])}\n"
    )


def meditate(player: Player) -> None:
    print("你盘膝而坐，运转功法静心修炼……")
    regen = min(player.max_qi - player.qi, 8)
    player.qi += regen
    exp_gain = random.randint(3, 7)
    player.gain_exp(exp_gain)
    print(f"灵力恢复 {regen} 点，获得 {exp_gain} 点修为。\n")


def rest(player: Player) -> None:
    print("你闭目调息，身体逐渐放松。")
    heal = min(player.max_health - player.health, 10)
    player.health += heal
    player.qi = min(player.qi + 4, player.max_qi)
    print(f"气血恢复 {heal} 点，灵力略有回升。\n")


def explore(player: Player) -> None:
    print("你踏入山林秘境，周围灵气氤氲……")
    event_roll = random.random()
    if event_roll < 0.25:
        find_loot(player)
    elif event_roll < 0.5:
        combat(player)
    elif event_roll < 0.7:
        encounter_hermit(player)
    elif event_roll < 0.85:
        explore_ruins(player)
    else:
        heart_demon_trial(player)


def find_loot(player: Player) -> None:
    loot_options = [
        ("灵草", 1, "你发现一株灵草，灵光闪烁。"),
        ("灵丹", 1, "你获得一颗丹药，散发丹香。"),
        ("灵石", random.randint(1, 3), "你拾起几枚灵石，冰凉入手。"),
        ("护心符", 1, "你拾得一张护心符，符纹微亮。"),
    ]
    item, amount, desc = random.choice(loot_options)
    print(desc)
    if item == "灵石":
        player.spirit_stones += amount
        print(f"获得灵石 {amount} 枚。\n")
    else:
        player.inventory[item] = player.inventory.get(item, 0) + amount
        print(f"获得 {item} {amount} 个。\n")


def combat(player: Player) -> None:
    beast_health = random.randint(8, 18)
    beast_attack = random.randint(3, 6)
    print(f"一只凶兽拦住去路！气血：{beast_health}，攻击：{beast_attack}\n")

    while beast_health > 0 and player.is_alive():
        if player.qi >= 5:
            damage = random.randint(4, 8) + player.stage_index
            player.qi -= 5
            print(f"你施展法术，造成 {damage} 点伤害。")
        else:
            damage = random.randint(1, 4)
            print(f"灵力不足，你挥剑造成 {damage} 点伤害。")
        beast_health -= damage
        if beast_health <= 0:
            print("凶兽被你斩杀！\n")
            reward_exp = random.randint(8, 14)
            player.gain_exp(reward_exp)
            player.spirit_stones += 1
            print(f"获得修为 {reward_exp} 点，灵石 +1。\n")
            return

        player.health -= beast_attack
        print(f"凶兽反击，你受到了 {beast_attack} 点伤害。")
        if not player.is_alive():
            if player.inventory.get("护心符", 0) > 0:
                player.inventory["护心符"] -= 1
                player.health = 1
                print("护心符化作光幕为你挡下致命一击，你气息微弱但仍存一线生机！\n")
            else:
                print("你倒在山林之中，修行之路暂告一段落……\n")
                return


def encounter_hermit(player: Player) -> None:
    print("你邂逅一位云游前辈，对方点出几句口诀。")
    insight = random.randint(5, 10)
    player.gain_exp(insight)
    player.fame += 1
    if player.inventory.get("灵草", 0) > 0:
        player.inventory["灵草"] -= 1
        player.inventory["灵丹"] = player.inventory.get("灵丹", 0) + 1
        print("你以灵草相赠，对方回赠一枚灵丹。")
    print(f"领悟增加 {insight} 点修为，声望提升。\n")


def explore_ruins(player: Player) -> None:
    print("你发现一座残破石殿，隐约有阵法残留。")
    discovery_roll = random.random()
    if discovery_roll < 0.4:
        player.inventory["护心符"] = player.inventory.get("护心符", 0) + 1
        print("你小心拆下一角符文石板，获得一张护心符。\n")
    elif discovery_roll < 0.75:
        exp_gain = random.randint(10, 18)
        player.gain_exp(exp_gain)
        player.fame += 2
        print(f"你领悟古阵残篇，修为提升 {exp_gain}，声望大涨。\n")
    else:
        damage = random.randint(4, 10)
        player.health = max(player.health - damage, 1)
        player.qi = max(player.qi - 5, 0)
        print(f"机关突发，你受创 {damage} 点气血，灵力受损。\n")


def heart_demon_trial(player: Player) -> None:
    print("浓郁的魔气侵袭心神，你落入心魔幻境！")
    if player.qi < 6:
        print("灵力不足，你被幻境所扰，心神疲惫。\n")
        player.health = max(player.health - 6, 1)
        player.exp = max(player.exp - 5, 0)
        return
    player.qi -= 6
    success = random.random() < 0.55 + player.stage_index * 0.05
    if success:
        reward = random.randint(8, 15)
        player.gain_exp(reward)
        player.fame += 1
        print(f"你稳住心神，斩破心魔，修为提升 {reward} 点。\n")
    else:
        player.health = max(player.health - 8, 1)
        print("心魔反噬，你气血受损，但也铭记教训。\n")


def alchemy(player: Player) -> None:
    if player.inventory.get("灵草", 0) < 1:
        print("你缺少灵草，无法炼丹。\n")
        return
    if player.qi < 8:
        print("灵力不足，暂时无法炼丹。\n")
        return
    player.inventory["灵草"] -= 1
    player.qi -= 8
    success = random.random() < 0.8
    if success:
        player.inventory["灵丹"] = player.inventory.get("灵丹", 0) + 1
        print("炼丹成功，丹香扑鼻！获得一枚灵丹。\n")
    else:
        print("炉火不稳，灵草化为青烟。\n")


def use_pill(player: Player) -> None:
    if player.inventory.get("灵丹", 0) < 1:
        print("你没有灵丹可用。\n")
        return
    player.inventory["灵丹"] -= 1
    heal = min(player.max_health - player.health, 15)
    player.health += heal
    qi_gain = min(player.max_qi - player.qi, 10)
    player.qi += qi_gain
    player.gain_exp(5)
    print(f"你服下一枚灵丹，气血恢复 {heal} 点，灵力恢复 {qi_gain} 点，修为提升。\n")


def visit_market(player: Player) -> None:
    print("你来到坊市，仙家商贾们低声叫卖。")
    print(
        "坊市交易：\n"
        "  [1] 购买灵草（1 灵石）\n"
        "  [2] 购买灵丹（2 灵石）\n"
        "  [3] 购买护心符（3 灵石）\n"
        "  [4] 以 2 灵石换取指点（修为+8）\n"
        "  [0] 离开坊市\n"
    )
    option = input("请选择交易：").strip()
    if option == "1":
        cost = 1
        if player.spirit_stones >= cost:
            player.spirit_stones -= cost
            player.inventory["灵草"] = player.inventory.get("灵草", 0) + 1
            print("你购得一株灵草。\n")
        else:
            print("灵石不足。\n")
    elif option == "2":
        cost = 2
        if player.spirit_stones >= cost:
            player.spirit_stones -= cost
            player.inventory["灵丹"] = player.inventory.get("灵丹", 0) + 1
            print("你购得一枚灵丹。\n")
        else:
            print("灵石不足。\n")
    elif option == "3":
        cost = 3
        if player.spirit_stones >= cost:
            player.spirit_stones -= cost
            player.inventory["护心符"] = player.inventory.get("护心符", 0) + 1
            print("你购得一张护心符。\n")
        else:
            print("灵石不足。\n")
    elif option == "4":
        cost = 2
        if player.spirit_stones >= cost:
            player.spirit_stones -= cost
            player.gain_exp(8)
            player.fame += 1
            print("你向老者求教一段真诀，修为精进。\n")
        else:
            print("灵石不足。\n")
    else:
        print("你离开坊市。\n")


def show_menu() -> None:
    print(
        "可选行动：\n"
        "  [1] 打坐修炼\n"
        "  [2] 探索秘境\n"
        "  [3] 炼制丹药\n"
        "  [4] 服用灵丹\n"
        "  [5] 调息小憩\n"
        "  [6] 查看状态\n"
        "  [7] 前往坊市\n"
        "  [0] 结束修行\n"
    )


def main() -> None:
    name = input("请输入道号：").strip() or "无名散修"
    player = Player(name=name)
    print(f"\n{name}踏入修行之路，开始寻找飞升之机。\n")

    while player.is_alive():
        show_menu()
        choice = input("请选择行动：").strip()
        print()
        if choice == "1":
            meditate(player)
        elif choice == "2":
            explore(player)
        elif choice == "3":
            alchemy(player)
        elif choice == "4":
            use_pill(player)
        elif choice == "5":
            rest(player)
        elif choice == "6":
            describe_player(player)
        elif choice == "7":
            visit_market(player)
        elif choice == "0":
            print("你暂时离开红尘修行。")
            break
        else:
            print("未知的选择，请重新输入。\n")

        if player.stage_index == len(STAGES) - 1 and player.exp >= 40:
            print("你积累的道韵冲破桎梏，化光而去，飞升仙界！")
            break

    print("修行已毕，感谢游玩。")


if __name__ == "__main__":
    main()
