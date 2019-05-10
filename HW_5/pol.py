import math

from time_decorator import timeit

a = 0
b = 0
print(not (a and b))
# def _get_best_word(self, fix_string, error=0, iteration=-1, node=0, small_error=0, big_err=0):
#     branches = self.tree[node][1]  # все возможные замены букв, идущие после этого префикса
#
#     # print("way {};  string {}".format(way, string))
#     def next_iteration(new_str, add_er=0):
#         orig_next_char = new_str[iteration]
#         left_part = new_str[:iteration]
#         right_part = new_str[iteration + 1:]
#         for char, new_node in branches.items():
#             if char == END_OF_WORD:
#                 continue
#             new_str = left_part + char + right_part
#             self._get_best_word(fix_string=new_str,
#                                 error=error + add_er + self._get_error(orig_next_char, char),
#                                 pointer=iteration,
#                                 node=new_node,
#                                 big_err=big_err)
#         return
#
#     current_char = self.tree[node][0]
#
#     if error > self.error_threshold:
#         return
#     if (END_OF_WORD in branches) and (len(fix_string) - 1 == iteration):
#         self._add_match(fix_string + current_char, error)
#         print("(local) \"" + fix_string + "\"" + " --:-- error: " + str(error))
#         return
#     if len(fix_string) - 1 == iteration:
#         # print("+++REJECTED++++ {}".format(string))
#         return
#
#     iteration += 1
#     next_iteration(fix_string)  # next letter
#
#     if big_err < 1:  # пусть добавление или удаление буквы может быть только 1 раз
#         big_err += 1
#         if len(fix_string) - iteration > 1:  # dell current letter
#             add_error = self._get_error(fix_string[iteration], EMPTY_LEX)
#             next_iteration(fix_string[:iteration] + fix_string[iteration + 1:], add_error)
#
#         # for symbol in branches:  # add letter
#         symbol = next(iter(branches))  # add any letter from current branch
#         add_error = self._get_error(EMPTY_LEX, symbol)
#         next_iteration(fix_string[:iteration] + symbol + fix_string[iteration:], add_error)
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
#
# def _get_best_word(self, fixed_string, error=0, iteration=-1, node=0, small_error=0, big_err=0):
#     branches = self.tree[node][1]  # все возможные замены букв, идущие после этого префикса
#
#     def next_iteration(new_str, add_er=0):
#         next_char = new_str[iteration]
#         for char, new_node in branches.items():
#             if char == END_OF_WORD:
#                 continue
#             new_str[iteration] = next_char
#             self._get_best_word(fixed_string=new_str,
#                                 error=error + add_er + self._get_error(next_char, char),
#                                 pointer=iteration,
#                                 node=new_node,
#                                 big_err=big_err)
#         return
#
#     current_char = self.tree[node][0]
#
#     if error > self.error_threshold:
#         return
#     if (END_OF_WORD in branches) and (len(fixed_string) - 1 == iteration):
#         self._add_match(fixed_string + current_char, error)
#         print("(local) \"" + fixed_string + "\"" + " --:-- error: " + str(error))
#         return
#     if len(fixed_string) - 1 == iteration:
#         # print("+++REJECTED++++ {}".format(string))
#         return
#
#     iteration += 1
#     next_iteration(fixed_string)  # next letter
#
#     if big_err < 1:  # пусть добавление или удаление буквы может быть только 1 раз
#         big_err = 1
#         if len(fixed_string) - iteration > 1:  # dell current letter
#             add_error = self._get_error(fixed_string[iteration], EMPTY_LEX)
#             next_iteration(fixed_string[:iteration] + fixed_string[iteration + 1:], add_error)
#
#         for symbol in branches:  # add letter
#             add_error = self._get_error(EMPTY_LEX, symbol)
#             next_iteration(fixed_string[:iteration] + symbol + fixed_string[iteration:], add_error)
#
