.PHONY: serve example_jieba clean

serve: env
	fab serve

example_jieba: env
	fab example_jieba

env: requirements.txt
	fab setup

clean:
	@rm -rf *.egg-info
	@rm -rf env
	@rm -rf build
	@rm -rf dist
	@rm -rf *.pyc
