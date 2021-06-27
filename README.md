# Schmancy

Automatic shm-reduplication

Repeat a word, putting a shm- before the vowel sound in the first syllable e.g. Fancy-Shmancy.

### Example Usage
```python
# reduplication on a word
print(reduplicate('fancy', repeat=True))
# fancy-shmancy

# reduplication on an entire sentence
# text = "The quick brown fox jumps over the lazy dog."
print(reduplicate(text))
# The shmuick shmown shmox shmumps shmover the shmazy shmog.
print(reduplicate(text, repeat=True))
#The quick-shmuick brown-shmown fox-shmox jumps-shmumps over-shmover the lazy-shmazy dog-shmog.
print(reduplicate(text, start='w'))
# The wuick wown wox wumps wover the wazy wog.
```