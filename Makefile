

.PHONY: run clean

serve: .setup
	fab serve

example_jieba: .setup
	fab example_jieba

.setup: setup.py
	fab setup
	> $@

clean:
	@rm -rf .setup
	@rm -rf *.egg-info
	@rm -rf env
	@rm -rf build
	@rm -rf dist
	@rm -rf *.pyc