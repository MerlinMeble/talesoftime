"""
services.py - Service layer for Tales of Time (raw SQL version).

Services orchestrate repositories and construct ViewModels.
The only change from the ORM version: from_model() → from_row(),
and form_data passes sqlite3.Row objects instead of ORM instances.
"""

from repositories.repositories import (
    CharacterRepository, ItemRepository, QuestRepository,
    InventoryRepository, CharacterQuestRepository, LookupRepository,
)
from viewmodels.viewmodels import (
    CharacterListViewModel, CharacterFormViewModel, CharacterViewModel,
    ItemListViewModel, ItemFormViewModel, ItemViewModel,
    QuestListViewModel, QuestFormViewModel, QuestViewModel,
    InventoryEntryViewModel, CharacterQuestViewModel,
    DashboardViewModel,
)


class CharacterService:
    def __init__(self):
        self._repo   = CharacterRepository()
        self._lookup = LookupRepository()

    def list_characters(self) -> CharacterListViewModel:
        return CharacterListViewModel.from_rows(self._repo.get_all())

    def get_character(self, character_id: int) -> CharacterViewModel:
        return CharacterViewModel.from_row(self._repo.get_by_id(character_id))

    def get_form_data(self, character_id: int = None) -> CharacterFormViewModel:
        return CharacterFormViewModel(
            classes    = self._lookup.get_classes(),
            species    = self._lookup.get_species(),
            alignments = self._lookup.get_alignments(),
            character  = self._repo.get_by_id(character_id) if character_id else None,
        )

    def create_character(self, form_data: dict) -> None:
        self._repo.create(form_data)

    def update_character(self, character_id: int, form_data: dict) -> None:
        self._repo.update(character_id, form_data)

    def delete_character(self, character_id: int) -> None:
        self._repo.delete(character_id)


class ItemService:
    def __init__(self):
        self._repo   = ItemRepository()
        self._lookup = LookupRepository()

    def list_items(self) -> ItemListViewModel:
        return ItemListViewModel.from_rows(self._repo.get_all())

    def get_form_data(self) -> ItemFormViewModel:
        return ItemFormViewModel(
            item_types = self._lookup.get_item_types(),
            rarities   = self._lookup.get_rarities(),
        )

    def create_item(self, form_data: dict) -> None:
        self._repo.create(form_data)

    def delete_item(self, item_id: int) -> None:
        self._repo.delete(item_id)


class QuestService:
    def __init__(self):
        self._repo   = QuestRepository()
        self._lookup = LookupRepository()

    def list_quests(self) -> QuestListViewModel:
        return QuestListViewModel.from_rows(self._repo.get_all())

    def get_form_data(self) -> QuestFormViewModel:
        return QuestFormViewModel(
            regions      = self._lookup.get_regions(),
            difficulties = self._lookup.get_difficulties(),
        )

    def create_quest(self, form_data: dict) -> None:
        self._repo.create(form_data)

    def delete_quest(self, quest_id: int) -> None:
        self._repo.delete(quest_id)


class InventoryService:
    def __init__(self):
        self._inv_repo  = InventoryRepository()
        self._item_repo = ItemRepository()

    def get_inventory(self, character_id: int) -> list:
        rows = self._inv_repo.get_for_character(character_id)
        return [InventoryEntryViewModel.from_row(r) for r in rows]

    def available_items(self) -> list:
        return self._item_repo.get_all()

    def add_item(self, character_id: int, item_id: int, quantity: int = 1) -> None:
        self._inv_repo.add_item(character_id, item_id, quantity)

    def remove_item(self, inventory_id: int) -> None:
        self._inv_repo.remove_item(inventory_id)


class QuestProgressService:
    def __init__(self):
        self._cq_repo    = CharacterQuestRepository()
        self._quest_repo = QuestRepository()

    def get_character_quests(self, character_id: int) -> list:
        rows = self._cq_repo.get_for_character(character_id)
        return [CharacterQuestViewModel.from_row(r) for r in rows]

    def available_quests(self) -> list:
        return self._quest_repo.get_all()

    def assign_quest(self, character_id: int, quest_id: int) -> None:
        self._cq_repo.assign(character_id, quest_id)

    def complete_quest(self, cq_id: int) -> None:
        self._cq_repo.complete(cq_id)


class DashboardService:
    def __init__(self):
        self._char_repo  = CharacterRepository()
        self._item_repo  = ItemRepository()
        self._quest_repo = QuestRepository()

    def get_dashboard(self) -> DashboardViewModel:
        return DashboardViewModel(
            total_characters = self._char_repo.count(),
            total_items      = self._item_repo.count(),
            total_quests     = self._quest_repo.count(),
        )
